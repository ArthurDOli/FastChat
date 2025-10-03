from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from models import User
from schemas import UserBase, UserPublic
from sqlalchemy.orm import Session
from database import getSession
import bcrypt
from security import create_access_token, get_current_user

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])
templates = Jinja2Templates(directory='templates')

@auth_router.get("/users/me", response_model=UserPublic, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário logado.
    """
    return current_user

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
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Essa rota recebe os dados do formulário, verifica as credenciais e retorna um token JWT em caso de sucesso
    """
    user = session.query(User).filter(User.email == username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha incorretos")
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}

@auth_router.get('/login', tags=['Authentication'])
async def login_page(request: Request):
    """
    Essa rota apenas mostra a página HTML com o formulário de login
    """
    return templates.TemplateResponse('login.html', context={"request": request})