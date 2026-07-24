import asyncio
import aiohttp
import anyio
import time
import yarl
from dataclasses import dataclass
from enum import StrEnum

type URL = yarl.URL | str


@dataclass
class DownloadFile:
    url: URL
    path: anyio.Path


class DownloadStatus(StrEnum):
    DOWNLOADING = "Downloading"
    OK = "Ok"
    WAITING = "Waiting"


@dataclass
class DownloadTask(DownloadFile):
    status: DownloadStatus = DownloadStatus.WAITING
    total_size: int = 0
    download_size: int = 0
    _old_download_size: int = 0
    speed: float = 0


class DownloadManager:
    def __init__(
        self,
    ):
        self.downloads = asyncio.Queue()  # 存储下载任务的队列

    async def run(self):
        while True:
            # await self.http_file_downloads.get()
            pass

    async def download_game(self):
        pass


class HttpDownloadManager:
    def __init__(
        self,
        workers_num: int = 8,
        steam: bool = True,
        steam_chunk_size=1024 * 1024 * 10,
    ):
        self.workers_num = workers_num
        self._file_download_tasks: asyncio.Queue[DownloadFile] = (
            asyncio.Queue()
        )  # 存储文件下载任务的队列
        self._file_status_dict: dict[URL, DownloadTask] = {}
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
            tasks.append(asyncio.create_task(self._show_task_progress()))
            await self._file_download_tasks.join()
            for task in tasks:
                task.cancel()
            # 等待直到所有工作任务都被取消。
            await asyncio.gather(*tasks, return_exceptions=True)

    async def worker(self, session: aiohttp.ClientSession):
        while True:
            task = await self._file_download_tasks.get()
            try:
                await self.download_one(session, task)
            except Exception:
                pass
            finally:
                self._file_download_tasks.task_done()

    async def download_one(self, session: aiohttp.ClientSession, task: DownloadFile):
        url = task.url
        path = task.path
        print(f"正在下载: {url} | {path}")
        await path.parent.mkdir(parents=True, exist_ok=True)
        async with session.get(url) as resp:
            resp.raise_for_status()
            total_size = resp.content_length or 0
            print(f"下载大小 {total_size / 1024 / 1024:.2f} MB")
            task_status = self._get_download_task(url)
            task_status.total_size = total_size
            task_status.status = DownloadStatus.DOWNLOADING
            if self.steam:
                download_size = 0
                async with await anyio.open_file(path, mode="wb") as f:
                    async for chunk in resp.content.iter_chunked(self.steam_chunk_size):
                        await f.write(chunk)
                        download_size += len(chunk)
                        task_status.download_size = download_size

            else:
                await path.write_bytes(await resp.read())

    def _get_download_task(self, url: URL):
        return self._file_status_dict[url]

    async def add(self, task: DownloadFile):
        if task.url not in self._file_status_dict:
            self._file_status_dict.update({task.url: DownloadTask(task.url, task.path)})
            await self._file_download_tasks.put(task)

    async def _show_task_progress(self):
        while True:
            for task in self._file_status_dict.values():
                task.speed = task.download_size - task._old_download_size
                task._old_download_size = task.download_size
            print(self._file_status_dict)
            await asyncio.sleep(1)


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
