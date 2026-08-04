import asyncio
import compression.zstd
from dataclasses import dataclass

import anyio

from . import hypcore, download, http
from .type import hyp_download_check, hyp_download_game_branches
from .proto import Sophon_pb as protobuf

cache_dir = anyio.Path("cache")
game_install_dir = anyio.Path("games")


@dataclass
class MatchManfiest:
    category_id: str
    matching_field: str


class GameDownload:
    def __init__(self, launcher: hypcore.HYPLauncher) -> None:
        self.launcher = launcher

    async def get_game_branches(self, game_ids: list[str] | None = None):
        game_branches = await self.launcher.get_game_branches(game_ids)
        return hyp_download_game_branches.Data.model_validate(game_branches)

    async def get_sophon_chunk_build(
        self, branch: str, package_id: str, password: str, tag: str | None = None
    ):
        chunk_build = await self.launcher.get_game_chunk_build(
            branch, package_id, password, tag
        )
        return hyp_download_check.Data.model_validate(chunk_build)

    async def download_game_chunk(
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

        download_manager = download.HttpDownloadManager()
        for manifest in match_manifest_list:
            await download_manager.add(
                download.DownloadTask(
                    f"{manifest.manifest_download.url_prefix}/{manifest.manifest.id}",
                    cache_dir / manifest.manifest.id,
                )
            )
        await download_manager.run()

        ChunkManifest_proto = protobuf.SophonChunkManifest()
        for match_manifest in match_manifest_list:
            manifest_id = match_manifest.manifest.id
            print(f"正在解压清单: {manifest_id}")
            manifest_file = compression.zstd.decompress(
                await (cache_dir / manifest_id).read_bytes()
            )
            await (cache_dir / f"{manifest_id}.decompress").write_bytes(manifest_file)
            chunk_manifest_data = ChunkManifest_proto.from_binary(manifest_file)
            json_string = chunk_manifest_data.to_json(always_emit_implicit=True)
            await (cache_dir / f"{manifest_id}.json").write_text(json_string)

            chunks_dir = game_install_dir / "chunks"

            for file in chunk_manifest_data.chunks:
                file_path = game_install_dir / file.file
                if await file_path.exists():
                    print(f"文件已存在: {file.file}, 检查长度")
                    if await download.get_file_size(file_path) == file.size:
                        print(f"文件长度匹配: {file.file}, 跳过下载")
                        continue
                    # md5 = await download.get_file_md5(file_path)
                    # print(md5)
                    # if md5 == file.md5:
                    #     print(f"文件md5匹配: {file.file},  跳过下载")
                    #     continue
                print(f"正在下载文件: {file.file}")
                download_manager = download.HttpDownloadManager()
                for chunk in file.chunks:
                    await download_manager.add(
                        download.DownloadTask(
                            f"{match_manifest.chunk_download.url_prefix}/{chunk.id}",
                            chunks_dir / chunk.id,
                            chunk.compressed_md5,
                        )
                    )
                await download_manager.run()

                file.chunks.sort(key=lambda x: x.offset)
                print(file.chunks)
                print(f"正在合并文件: {file.file}")
                await file_path.parent.mkdir(parents=True, exist_ok=True)
                async with await anyio.open_file(file_path, "wb") as f:
                    for chunk in file.chunks:
                        chunk_file_path = chunks_dir / chunk.id
                        chunk_file = compression.zstd.decompress(
                            await chunk_file_path.read_bytes()
                        )
                        await f.seek(chunk.offset)
                        await f.write(chunk_file)
                for chunk in file.chunks:
                    print(f"正在删除临时文件: {chunks_dir / chunk.id}")
                    await (chunks_dir / chunk.id).unlink(missing_ok=True)
                    if await (chunks_dir / chunk.id).exists():
                        print(f"删除失败: {chunk.id}")

                


if __name__ == "__main__":
    gd = GameDownload(
        hypcore.HYPLauncher(hypcore.LaucherArea.CN, hypcore.LauncherType.CN)
    )

    async def main():
        game_branches_data = await gd.get_game_branches(["x6znKlJ0xK"])
        chunk_build_data = await gd.get_sophon_chunk_build(
            "main", "FfGDa3bsvp", "FJCF1CT6Z4nz"
        )
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
        await gd.download_game_chunk(chunk_build_data, ck_list)

    asyncio.run(main())
