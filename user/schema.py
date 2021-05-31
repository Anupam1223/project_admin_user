from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    status: int
    super_user: int


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    status: int
    super_user: int


class TokenData(BaseModel):
    username: Optional[str] = None
