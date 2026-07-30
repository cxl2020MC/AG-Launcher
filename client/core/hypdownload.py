import asyncio
import compression.zstd
from dataclasses import dataclass

import anyio

from . import hypcore, download, http
from .type import hyp_download_check, hyp_download_game_branches
from .proto import Sophon_pb2 as protobuf
from google.protobuf import json_format

cache_dir = anyio.Path("cache")


@dataclass
class MatchManfiest:
    category_id: str
    matching_field: str


class GameDownload:
    def __init__(self, launcher: hypcore.HYPLauncher) -> None:
        self.launcher = launcher
        self.download_manager = download.HttpDownloadManager()

    async def get_game_branches(self, game_ids: list[str] | None = None):
        game_branches = await self.launcher.get_game_branches(game_ids)
        return hyp_download_game_branches.Data.model_validate(game_branches)

    async def get_sophon_chunk_build(
        self, branch: str, package_id: str, password: str, tag: str | None = None
    ):
        chunk_build = await self.launcher.get_game_chunk_build(
            branch, package_id, password
        )
        return hyp_download_check.Data.model_validate(chunk_build)

    async def get_game(
        self,
        chunk_build: hyp_download_check.Data,
        match_manifests: list[tuple[str, str]],
    ):
        match_manifest_list: list[hyp_download_check.ManifestItem] = []
        for manifest in chunk_build.manifests:
            category_id = manifest.category_id
            matching_field = manifest.matching_field
            if (category_id, matching_field) in match_manifests:
                print(
                    f"匹配到分类: {category_id} | {matching_field} ({manifest.category_name})"
                )
                match_manifest_list.append(manifest)
                await self.download_manager.add(
                    download.DownloadTask(
                        f"{manifest.manifest_download.url_prefix}/{manifest.manifest.id}",
                        cache_dir / manifest.manifest.id,
                    )
                )
        await self.download_manager.run_background()
        await self.download_manager.wait_download_ok()

        ChunkManifest_proto = protobuf.SophonChunkManifest()

        for match_manifest in match_manifest_list:
            manifest_file = compression.zstd.decompress(
                await (cache_dir / match_manifest.manifest.id).read_bytes()
            )
            await (cache_dir / f"{match_manifest.manifest.id}.decompress").write_bytes(manifest_file)
            # ChunkManifest = ChunkManifest_proto.ParseFromString(manifest_file)
            json_string = json_format.MessageToJson(ChunkManifest_proto)
            await (cache_dir / f"{match_manifest.manifest.id}.json").write_text(json_string)


if __name__ == "__main__":
    gd = GameDownload(
        hypcore.HYPLauncher(hypcore.LaucherArea.CN, hypcore.LauncherType.CN)
    )

    async def main():
        game_branches_data = await gd.get_game_branches(["x6znKlJ0xK"])
        chunk_build_data = await gd.get_sophon_chunk_build("main", "FfGDa3bsvp", "FJCF1CT6Z4nz")
        cgs: list[hyp_download_game_branches.Category] = []
        for categorie in game_branches_data.game_branches[0].main.categories:
            if (
                hyp_download_game_branches.CategoryType.CATEGORY_TYPE_RESOURCE
                is categorie.type
            ):
                if (
                    hyp_download_game_branches.ScenarioType.CATEGORY_SCENARIO_BASE
                    in categorie.scenarios
                ):
                    cgs.append(categorie)
        print(cgs)
        ck_list = []
        for i in cgs:
            ck_list.append((i.category_id, i.matching_field))
        print(ck_list)
        await gd.get_game(chunk_build_data, ck_list)

    asyncio.run(main())
