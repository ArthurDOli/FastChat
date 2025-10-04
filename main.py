# uvicorn main:app --reload

from fastapi import FastAPI
from auth import auth_router
from chat import chat_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)