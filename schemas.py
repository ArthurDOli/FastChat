from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    class Config:
        from_attributes = True