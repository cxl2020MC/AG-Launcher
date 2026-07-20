import asyncio
import aiohttp


class DownloadManager:
    def __init__(
        self,
    ):
        self.downloads = asyncio.Queue()  # 存储下载任务的队列
        self.http_file_downloads = asyncio.Queue() # 存储文件下载任务的队列

    async def run(self):
        while True:
            await self.http_file_downloads.get()