from typing import Any
from enum import StrEnum
from pydantic import BaseModel
from . import hyp_api


class CategoryType(StrEnum):
    CATEGORY_TYPE_RESOURCE = "CATEGORY_TYPE_RESOURCE"
    CATEGORY_TYPE_AUDIO = "CATEGORY_TYPE_AUDIO"


class ScenarioType(StrEnum):
    CATEGORY_SCENARIO_FULL = "CATEGORY_SCENARIO_FULL"
    CATEGORY_SCENARIO_BASE = "CATEGORY_SCENARIO_BASE"


class Category(BaseModel):
    category_id: str
    matching_field: str
    type: CategoryType  # 字段名与 JSON 中的 "type" 一致
    scenarios: list[ScenarioType]


class Game(BaseModel):
    id: str
    biz: str


class Main(BaseModel):
    package_id: str
    branch: str
    password: str
    tag: str
    diff_tags: list[str]
    categories: list[Category]
    required_client_version: str


class GameBranch(BaseModel):
    game: Game
    main: Main
    pre_download: Any | None = None  # JSON 中为 null，可能为其他类型
    enable_base_pkg_predownload: bool


class Data(BaseModel):
    game_branches: list[GameBranch]


type Response = hyp_api.Response[Data]
