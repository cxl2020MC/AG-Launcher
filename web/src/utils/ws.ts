import { useGameStore } from '@/stores/game';


const params = new URLSearchParams(window.location.search);

const ws_url = params.get('ws_url') ? (params.get('ws_url') as string) : '//localhost:8000/ws';

console.log("WebSocket URL:", ws_url);


let ws: WebSocket | null = null;
if (ws_url) {
    ws = createWebSocket(ws_url);
}

console.log("WebSocket instance:", ws);

function createWebSocket(ws_url: string): WebSocket {
    const ws = new WebSocket(ws_url)

    // 连接成功
    ws.addEventListener('open', () => {
        console.log("连接已建立");
    });

    // 接收消息
    ws.addEventListener('message', (event) => {
        console.log(event)
        console.log("收到消息:", event.data);
        const jsonData = JSON.parse(event.data);
        console.log("解析后的 JSON 数据:", jsonData);
        if (jsonData.type === "update") {
            console.log("收到更新消息:", jsonData);
            // 在这里处理更新消息，例如更新页面内容
            if (jsonData.action == "update_bg") {
                console.log("收到背景更新消息:", jsonData);
                // 在这里处理背景更新逻辑
                const store = useGameStore();
                store.$state = jsonData.data;
            }
        }
    });

    // 连接关闭
    ws.addEventListener('close', () => {
        console.log("连接已关闭");
        console.log("尝试重新连接...");
        setTimeout(() => {
            createWebSocket(ws_url);
        }, 1000);
    });

    // 出错处理
    ws.addEventListener('error', (error) => {
        console.error("WebSocket 错误:", error);

    });

    return ws;
};


