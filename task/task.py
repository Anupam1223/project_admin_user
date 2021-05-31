from user import schema
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .schema import view_assigned_project
from . import crud
from user.user import oauth2_scheme, get_user
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Dict


router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def get_admin_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_user)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("user")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    view_user_project = crud.check_admin(db, username=token_data.username)
    if view_user_project is None:
        raise credentials_exception
    return view_user_project


@router.get("/view_user_project", tags=["Task"])
async def view_user_project(
    user_project: Dict = Depends(get_admin_user),
):
    return user_project
