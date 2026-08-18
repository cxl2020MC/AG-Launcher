import asyncio
import hashlib
import time
from dataclasses import dataclass
from enum import StrEnum

# import aiohttp
import anyio
import yarl
from niquests import AsyncSession

type URL = str | yarl.URL


# @dataclass
# class DownloadFile:
#     url: URL
#     path: anyio.Path
#     md5: str | None = None


class DownloadStatus(StrEnum):
    DOWNLOADING = "Downloading"
    OK = "Ok"
    WAITING = "Waiting"


@dataclass
class DownloadTask:
    url: URL
    path: anyio.Path
    md5: str | None = None

    status: DownloadStatus = DownloadStatus.WAITING
    total_size: int = 0
    download_size: int = 0
    progress: float = 0
    _old_download_size: int = 0
    speed: float = 0
    _latest_update_time: float = 0
    error: str | None = None

    def update_status(self, check_size: int):
        self.download_size += check_size
        if self.total_size:
            self.progress = self.download_size / self.total_size
        use_time = time.monotonic() - self._latest_update_time
        if use_time >= 0.5:
            self.speed = (self.download_size - self._old_download_size) / use_time
            self._old_download_size = self.download_size
            self._latest_update_time = time.monotonic()


class HttpDownloadManager:
    def __init__(
        self,
        workers_num: int = 8,
        steam_chunk_size=1024 * 1024 * 1,
    ):
        self.workers_num = workers_num
        self._file_download_tasks: list[DownloadTask] = []
        self.steam_chunk_size = steam_chunk_size  # 默认1MB
        self._close: bool = False
        self._task_group: asyncio.TaskGroup | None = None

    async def run(self):
        async with AsyncSession(multiplexed=True, happy_eyeballs=True) as session:
            sem = asyncio.Semaphore(self.workers_num)
            async with asyncio.TaskGroup() as tg:
                self._task_group = tg
                for download_task in self._file_download_tasks:
                    tg.create_task(
                        self.download_one(sem, session, download_task),
                        name=f"download-worker-{download_task.url}",
                    )

    async def run_background(self):
        asyncio.create_task(self.run(), name="下载协程")

    async def download_one(
        self, sem: asyncio.Semaphore, session: AsyncSession, task: DownloadTask
    ):
        url = task.url
        path = task.path
        async with sem:
            print(f"正在下载: {task}")
            if task.md5 and await path.exists():
                print(f"文件已存在: {path}, 检查md5")
                md5 = await get_file_md5(path)
                print(md5)
                if md5 == task.md5:
                    print(f"文件md5匹配: {path}, 跳过下载")
                    return
            await path.parent.mkdir(parents=True, exist_ok=True)

            resp = await session.get(str(url), stream=True)
            await session.gather(resp)
            resp.raise_for_status()
            total_size = int(resp.headers.get("content-length") or 0)
            print(f"下载大小 {transform_file_size(total_size)}")
            task.total_size = total_size
            task.status = DownloadStatus.DOWNLOADING
            async with await anyio.open_file(path, mode="wb") as f:
                async for chunk in await resp.iter_content(self.steam_chunk_size):
                    await f.write(chunk)
                    task.update_status(len(chunk))

    async def add(self, task: DownloadTask):
        if task.url not in self._file_download_tasks:
            self._file_download_tasks.append(task)

    def get_all_download_progress(self):
        return self._file_download_tasks.copy()

    async def show_progress(self, update_time: float = 1):
        async def show_progress(self):
            while True:
                if self._close:
                    break
                for task in self.get_all_download_progress():
                    print(task)
                await asyncio.sleep(update_time)

        return asyncio.create_task(show_progress(self))


async def get_file_md5(path: anyio.Path, chunk_size: int = 1024 * 1024 * 10) -> str:
    md5_hash = hashlib.md5()
    async with await anyio.open_file(path, mode="rb") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            await asyncio.to_thread(md5_hash.update, chunk)
    return md5_hash.hexdigest()


async def get_file_size(path: anyio.Path) -> int:
    size = await path.stat()
    return size.st_size


def transform_file_size(size: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


if __name__ == "__main__":
    dm = HttpDownloadManager()

    async def main():
        await dm.add(
            DownloadTask(
                "https://autopatchcn.juequling.com/package_download/op/client_app/download/20260529101913_kArtwDVsrOev13EB/VolumeZip/juequling_3.0.0_AS.zip.001",
                anyio.Path("./juequling_3.0.0_AS.zip.001"),
            )
        )
        await dm.add(
            DownloadTask(
                "https://autopatchcn.juequling.com/package_download/op/client_app/download/20260529101913_kArtwDVsrOev13EB/VolumeZip/juequling_3.0.0_AS.zip.002",
                anyio.Path("./juequling_3.0.0_AS.zip.002"),
            )
        )
        await dm.show_progress()
        # asyncio.create_task(dm.run())
        await dm.run()
        # await dm.close()

    asyncio.run(main())
