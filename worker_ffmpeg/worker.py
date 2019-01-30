import asyncio
import logging
import datetime
import uuid

from sqlalchemy import and_
from sqlalchemy.sql import select

from .models import transcode_task, TranscodeTask

log = logging.getLogger(__name__)


class BaseWorker(object):

    def __init__(self, batch_size=1, pool_size=1, sleep_interval=5):
        self.batch_size = batch_size
        self.pool_size = pool_size
        self.loop = asyncio.get_event_loop()
        self.pool = asyncio.Queue(maxsize=pool_size)
        self.sleep_interval = sleep_interval

    def close(self):
        for task in asyncio.Task.all_tasks():
            task.cancel()
        self.loop.close()

    async def work(self):
        pass

    async def process(self):
        while True:
            try:
                item, = await self.pool.get()
                await self.process_item(item)
            except asyncio.CancelledError:
                log.warning("Cancelling process")

    async def fetch(self, *args):
        pass

    async def process_item(self, *args):
        pass

    async def sleep(self, timeout=None):
        timeout = timeout or self.sleep_interval
        timeout = max(timeout, 0.1)
        await asyncio.sleep(timeout)

    def start(self):
        try:
            self.loop.run_until_complete(self.work())
        except KeyboardInterrupt:
            self.close()


class DBWorker(BaseWorker):

    def __init__(self, batch_size=1, tx_manager=None, pool_size=1, sleep_interval=5):
        """
        :type batch_size: int
        :type tx_manager: worker_ffmpeg.transaction.TxManager
        :type pool_size: int
        :type sleep_interval: int
        """
        super(DBWorker, self).__init__(batch_size, pool_size, sleep_interval)
        self.sleep_interval = sleep_interval
        self.tx_manager = tx_manager

    async def work(self):
        for i in range(self.pool_size):
            asyncio.ensure_future(self.process())
        while True:
            try:
                if not self.pool.full():
                    with self.tx_manager.begin() as tx:
                        item = await self.fetch(tx)
                        if item is not None:
                            self.pool.put_nowait(item)
                await self.sleep()
            except asyncio.QueueFull:
                continue
            except asyncio.CancelledError:
                log.warning("Cancelling work")

    async def fetch(self, tx):
        """
        :type tx: sqlalchemy.orm.session.Session
        :rtype: tuple(int,)
        """
        record_id = tx.execute(select([transcode_task.c.id]).where(
            and_(transcode_task.c.expiry < datetime.datetime.utcnow(),
                 transcode_task.c.uuid == None)
        )).fetchone()
        return record_id

    async def lock_row(self, tx, record_id):
        """
        :type tx: sqlalchemy.orm.session.Session
        :type record_id: int
        :rtype: .models.TranscodeTask
        """
        record = tx.execute(transcode_task.update().where(
            transcode_task.c.id == record_id
        ).values(
            uuid=str(uuid.uuid4())
        ).returning(*transcode_task.columns)).fetchone()
        return TranscodeTask(*record)

    async def process_row(self, tx, record):
        """
        :type tx: sqlalchemy.orm.session.Session
        :type record: .models.TranscodeTask
        :rtype: None
        """
        log.warning(record)

        tx.execute(transcode_task.update().where(
            transcode_task.c.id == record.id
        ).values(
            uuid = None
        ))

    async def process_item(self, record_id):
        """Co-routine to perform work"""
        with self.tx_manager.begin() as tx:
            record = await self.lock_row(tx, record_id)
            if record is None:
                pass
        with self.tx_manager.begin() as tx:
            await self.process_row(tx, record)
