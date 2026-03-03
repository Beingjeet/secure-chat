from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

active_connections: List[WebSocket] = []

@app.get("/")
async def get():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # 🔥 No encryption here anymore
            # Just forward message

            for connection in active_connections:
                await connection.send_text(data)

    except:
        active_connections.remove(websocket)
      