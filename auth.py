from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from models import User
from schemas import UserBase
from sqlalchemy.orm import Session
from database import getSession
import bcrypt

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])
templates = Jinja2Templates(directory='templates')


##### REGISTER #####

@auth_router.post('/register', tags=['Authentication'])
async def create_account(
    session: Session = Depends(getSession),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Esta  rota recebe os dados do formulário e cria o usuário no banco
    """
    user = session.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um usuário com esse email")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password.decode()
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return RedirectResponse(url='/auth/login', status_code=status.HTTP_303_SEE_OTHER)

@auth_router.get('/register', tags=['Authentication'])
async def create_account_page(request: Request):
    """
    Esta rota apenas mostra a página HTML com o formulário de registro
    """
    return templates.TemplateResponse('register.html', context={"request": request})


##### LOGIN #####

@auth_router.post('/login', tags=['Authentication'])
async def login(
    session: Session = Depends(getSession),
    email: str = Form(...),
    password: str = Form(...)
):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="E-mail ou senha incorretos")
    return {"message": f"Login bem-sucedido! Bem-vindo, {user.username}!"}

@auth_router.get('/login', tags=['Authentication'])
async def login_page(request: Request):
    """
    Essa rota apenas mostra a página HTML com o formulário de login
    """
    return templates.TemplateResponse('login.html', context={"request": request})