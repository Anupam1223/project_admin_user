from pydantic import BaseModel
from typing import Optional

# ------model used to return the token--------
class Token(BaseModel):
    access_token: str
    token_type: str


# --------------------------------------------

# -model used for user related response-------
class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True


# --------------------------------------------

# -model used for creating user---------------
class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    status: int
    super_user: int


# --------------------------------------------

# --model designed especially to hide password
class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    status: int
    super_user: int


# --------------------------------------------

# ------------For manipulating token data-----
class TokenData(BaseModel):
    username: Optional[str] = None


# --------------------------------------------
