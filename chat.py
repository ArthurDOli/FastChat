from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from security import get_current_user_from_websocket
from fastapi.templating import Jinja2Templates
from ws_manager import manager
from models import User

chat_router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='templates')

@chat_router.get('/')
async def get_chat_page(request: Request):
    return templates.TemplateResponse('chat.html', context={"request": request})

@chat_router.websocket('/ws')
async def chat_websocket(websocket: WebSocket, current_user: User = Depends(get_current_user_from_websocket)):
    username = current_user.username
    await manager.connect(websocket, username)
    await manager.broadcast_to_others({"sender": "System", "message": f"Usuário '{username}' entrou no chat"}, username)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast({"sender": username, "message": data['text']})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_to_others({"sender": "System", "message": f"Usuário '{username}' saiu do chat"}, username)