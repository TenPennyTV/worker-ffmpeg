import asyncio
from worker_ffmpeg import worker, transaction

if __name__ == '__main__':
    worker = worker.DBWorker(tx_manager=transaction.tx_manager)
    asyncio.run(worker.start())
