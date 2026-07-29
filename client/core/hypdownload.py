import asyncio
import compression.zstd

import anyio

from . import hypcore, download, http
from .type import hyp_download_check, hyp_download_game_branches


class GameDownload:
    def __init__(self, launcher: hypcore.HYPLauncher) -> None:
        self.launcher = launcher
        self.download_manager = download.HttpDownloadManager()

    async def get_game_branches(self):
        game_branches = await self.launcher.get_game_branches()
        return hyp_download_game_branches.Data.model_validate(game_branches)

    async def get_sophon_chunk_build(
        self, branch: str, package_id: str, password: str, tag: str | None = None
    ):
        chunk_build = await self.launcher.get_game_chunk_build(
            branch, package_id, password
        )
        return hyp_download_check.Data.model_validate(chunk_build)

    async def get_game(self, chunk_build: hyp_download_check.Data, category_ids: list[str]):
        for manifest in chunk_build.manifests:
            category_id = manifest.category_id
            if category_id in category_ids:
                print(f"匹配到分类: {category_id} ({manifest.category_name})")
                await self.download_manager.add(download.DownloadTask(f"{manifest.manifest_download.url_prefix}/{manifest.manifest.id}", anyio.Path(manifest.manifest.id)))

    async def download_game_category(self):
        pass
