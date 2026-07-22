import asyncio
import aiohttp
import anyio
import time
import yarl
from dataclasses import dataclass

type URL = yarl.URL | str


@dataclass
class DownloadFile:
    url: URL
    path: anyio.Path


class DownloadManager:
    def __init__(
        self,
    ):
        self.downloads = asyncio.Queue()  # 存储下载任务的队列

    async def run(self):
        while True:
            # await self.http_file_downloads.get()
            pass


class HttpDownloadManager:
    def __init__(
        self,
        workers_num: int = 8,
        steam: bool = True,
        steam_chunk_size=1024 * 1024 * 10,
    ):
        self.workers_num = workers_num
        self.file_downloads: asyncio.Queue[DownloadFile] = (
            asyncio.Queue()
        )  # 存储文件下载任务的队列
        self.steam: bool = steam
        self.steam_chunk_size = steam_chunk_size  # 默认10MB

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(self.workers_num + 1):
                task = asyncio.create_task(
                    self.worker(session), name=f"download-worker-{i}"
                )
                tasks.append(task)
            await self.file_downloads.join()
            for task in tasks:
                task.cancel()
            # 等待直到所有工作任务都被取消。
            await asyncio.gather(*tasks, return_exceptions=True)

    async def worker(self, session: aiohttp.ClientSession):
        while True:
            task = await self.file_downloads.get()
            try:
                await self.download_one(session, task.url, task.path)
            except Exception:
                pass
            finally:
                self.file_downloads.task_done()

    async def download_one(
        self, session: aiohttp.ClientSession, url: URL, path: anyio.Path
    ):
        print(f"正在下载: {url} | {path}")
        await path.parent.mkdir(parents=True, exist_ok=True)
        async with session.get(url) as resp:
            resp.raise_for_status()
            total_size = resp.content_length or 0
            print(f"下载大小 {total_size / 1024 / 1024:.2f} MB")
            if self.steam:
                download_size = 0
                start_time = time.monotonic()
                async with await anyio.open_file(path, mode="wb") as f:
                    async for chunk in resp.content.iter_chunked(self.steam_chunk_size):
                        await f.write(chunk)
                        download_size += len(chunk)
                        end_time = time.monotonic()
                        if total_size:
                            print(
                                f"{path} 已下载: {download_size / 1024 / 1024:.2f}MB/{total_size / 1024 / 1024:.2f}MB ({(download_size / total_size) * 100:.2f}%) {(len(chunk) / (end_time - start_time)) / 1024 / 1024:.2f}MB/s",
                                end="\r",
                            )
                        start_time = time.monotonic()

            await path.write_bytes(await resp.read())

    async def add(self, task: DownloadFile):
        return await self.file_downloads.put(task)


if __name__ == "__main__":
    dm = HttpDownloadManager()

    async def main():
        await dm.add(
            DownloadFile(
                "https://autopatchcn.juequling.com/package_download/op/client_app/download/20260529101913_kArtwDVsrOev13EB/VolumeZip/juequling_3.0.0_AS.zip.001",
                anyio.Path("./juequling_3.0.0_AS.zip.001"),
            )
        )
        # await dm.add(DownloadFile("https://autopatchcn.juequling.com/package_download/op/client_app/download/20260529101913_kArtwDVsrOev13EB/VolumeZip/juequling_3.0.0_AS.zip.002", anyio.Path("./juequling_3.0.0_AS.zip.002")))

        await dm.run()

    asyncio.run(main())
