import json
import asyncio
import aiohttp
from compression import zstd
from pathlib import Path

from core.proto import Sophon_pb2 as protobuf

path = Path("./logs")

zstd_manifest_file_path = (
    path / "manifest_508508b8b6cf315c_4e2e19da9d8ce5b4c3d5df27060a38a9"
)
zstd_manifest_file = zstd_manifest_file_path.read_bytes()
manifest_file = zstd.decompress(zstd_manifest_file)
manifest_file_path = (
    path / "manifest_508508b8b6cf315c_4e2e19da9d8ce5b4c3d5df27060a38a9.decompressed"
)
manifest_file_path.write_bytes(manifest_file)

print(dir(protobuf))
if hasattr(protobuf, "SophonChunkManifest"):
    ChunkManifest_proto = protobuf.SophonChunkManifest()
    ChunkManifest = ChunkManifest_proto.ParseFromString(manifest_file)
    print(ChunkManifest)
    print(ChunkManifest_proto)
    from google.protobuf import json_format

    json_string = json_format.MessageToJson(ChunkManifest_proto)
    # print(json_string)
    json_file = path / "manifest.json"
    json_file.write_text(json_string)
