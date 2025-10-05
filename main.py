# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth import auth_router
from chat import chat_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(chat_router)