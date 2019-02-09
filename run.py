import asyncio
from worker_ffmpeg import worker, transaction
from worker_ffmpeg.spaces import init_s3

if __name__ == '__main__':
    init_s3()
    worker = worker.DBWorker(tx_manager=transaction.tx_manager)
    asyncio.run(worker.start())
