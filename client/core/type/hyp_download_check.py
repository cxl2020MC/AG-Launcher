from pydantic import BaseModel
from . import hyp_api

class ManifestInfo(BaseModel):
    id: str
    checksum: str
    compressed_size: int          # JSON 中为字符串数字，Pydantic 自动转换
    uncompressed_size: int


class DownloadInfo(BaseModel):
    encryption: int
    password: str
    compression: int
    url_prefix: str
    url_suffix: str


class Stats(BaseModel):
    compressed_size: int
    uncompressed_size: int
    file_count: int
    chunk_count: int


class ManifestItem(BaseModel):
    category_id: str
    category_name: str
    manifest: ManifestInfo
    chunk_download: DownloadInfo
    manifest_download: DownloadInfo
    matching_field: str
    stats: Stats
    deduplicated_stats: Stats


class Data(BaseModel):
    build_id: str
    tag: str
    manifests: list[ManifestItem]


type Response = hyp_api.Response[Data]
