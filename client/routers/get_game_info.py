from core import hypcore
from core.type import request
from fastapi.websockets import WebSocket

from fastapi import APIRouter

router = APIRouter()


async def read_game_info(data: request.RequestModel, websocket: WebSocket):
    return await hypcore.HYPLauncher(
        hypcore.LaucherArea.CN, hypcore.Launcher.CN
    ).get_games()


@router.get("/games_info")
async def get_games_info(area: hypcore.LaucherArea, launcher: hypcore.Launcher):
    return await hypcore.HYPLauncher(area, launcher).get_games()

@router.get("/game_info")
async def get_game_info(area: hypcore.LaucherArea, launcher: hypcore.Launcher, game_id: str | None = None, game_biz: str | None = None):
    return await hypcore.HYPLauncher(area, launcher).get_game(game_id=game_id, game_biz=game_biz)
