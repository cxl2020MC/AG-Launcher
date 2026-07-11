from core import hypcore
from core.type import request
from fastapi.websockets import WebSocket

async def read_game_info(data: request.RequestModel, websocket: WebSocket):
    return await hypcore.HYPLauncher(hypcore.LaucherArea.CN, hypcore.Launcher.CN).get_games()