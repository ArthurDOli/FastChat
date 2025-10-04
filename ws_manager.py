from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, websocket: WebSocket):
        username_to_remove = None
        for username, connection in self.active_connections.items():
            if connection == websocket:
                username_to_remove = username
                break
        if username_to_remove:
            del self.active_connections[username_to_remove]
            return username_to_remove
        return None

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)
    
    async def broadcast_to_others(self, message: dict, sender_username: str):
        for username, connection in self.active_connections.items():
            if username != sender_username:
                await connection.send_json(message)

manager = ConnectionManager()