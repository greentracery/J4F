#
# см. https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients
#
from fastapi import WebSocket, WebSocketDisconnect

class WSConnectionManager:
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def send_text(self, message: str, websocket: WebSocket):
        if websocket.application_state.CONNECTED:
            await websocket.send_text(message)

    async def broadcast_text(self, message: str):
        for connection in self.active_connections:
            if connection.application_state.CONNECTED:
                await connection.send_text(message)

    async def send_json(self, message, websocket: WebSocket):
        if websocket.application_state.CONNECTED:
            await websocket.send_json(message)

    async def broadcast_json(self, message):
        for connection in self.active_connections:
            if connection.application_state.CONNECTED:
                await connection.send_json(message)
