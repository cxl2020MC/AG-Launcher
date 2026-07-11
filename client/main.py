import threading
import webview

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from routers import get_game_info
from core.type import request

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(dict(request.RequestModel(type="connection", action="connected")))
    while True:
        data = await websocket.receive_json()
        print(f"收到消息： {data}")
        data = request.RequestModel.model_validate(data)
        if data.type == "request":
            if data.action == "get_game_info":
                game_info = await get_game_info.read_game_info(data, websocket)
                await websocket.send_json(dict(type="response", action="get_game_info", data=game_info))
            else:
                await websocket.send_json(dict(type="error", action=data.action, data={"message": "未知的请求动作"}))
        await websocket.send_json(dict(data))

app.mount("/", StaticFiles(directory="static"), name="static")

def main():
    def run_server():
        import uvicorn
        uvicorn.run(app)
    threading.Thread(target=run_server).start()


def on_closing():
    print("Window is closing...")
    import os
    import signal
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
    main()
    window = webview.create_window(
        'Simple browser', 'http://localhost:5173', width=1280, height=720+30)
    if window is None:
        print("Failed to create webview window.")
        exit(1)
    # 添加关闭事件处理
    window.events.closing += on_closing

    webview.start(debug=True)
