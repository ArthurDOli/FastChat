from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ws_manager import manager

chat_router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='templates')

@chat_router.get('/', tags=['Chat'])
async def chat_page(request: Request):
    return templates.TemplateResponse('chat.html', context={"request": request})

@chat_router.websocket('/ws/{client_id}')
async def chat_websocket(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")