from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

# Simple WebSocket echo/broadcast
class ConnectionManager:
    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.discard(websocket)

    async def broadcast(self, message: str):
        for ws in list(self.active):
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(ws)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(f"echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws)

# Simple Server-Sent Events endpoint
@router.get("/sse")
async def sse():
    async def event_stream():
        i = 0
        while True:
            yield f"data: tick {i}\n\n"
            i += 1
            await asyncio.sleep(2)
    return StreamingResponse(event_stream(), media_type="text/event-stream")
