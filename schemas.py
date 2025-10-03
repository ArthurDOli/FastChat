from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True