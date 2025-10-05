from security import create_access_token, get_current_user, create_refresh_token, get_user_from_refresh_token
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from schemas import UserBase, UserPublic
from sqlalchemy.orm import Session
from database import getSession
from models import User
import bcrypt

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])
templates = Jinja2Templates(directory='templates')

@auth_router.get("/users/me", response_model=UserPublic, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Returns the authenticated user's data.
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
    This route receives the form data and creates the user in the database.
    """
    user = session.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already in use.")
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
    return RedirectResponse(url='/chat', status_code=status.HTTP_303_SEE_OTHER)

@auth_router.get('/register', tags=['Authentication'])
async def create_account_page(request: Request):
    """
    This route simply displays the HTML page with the registration form.
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
    This route receives the form data, verifies the credentials, and returns a JWT token upon a successful verification.
    """
    user = session.query(User).filter(User.email == username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail or password incorrect.")
    access_token = create_access_token(data={'sub': user.email})
    refresh_token = create_refresh_token(data={'sub': user.email})
    return {
        'access_token': access_token, 
        'refresh_token': refresh_token,
        'token_type': 'bearer'
        }

@auth_router.post('/refresh', tags=['Authentication'])
async def refresh_token(current_user: User = Depends(get_user_from_refresh_token)):
    """
    Receives a refresh token and returns a new access token.
    """
    new_access_token = create_access_token(data={'sub': current_user.email})
    return {'access_token': new_access_token, 'token_type': 'bearer'}