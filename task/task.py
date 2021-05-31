from user import schema
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .schema import Create_task
from . import crud
from user.user import oauth2_scheme, get_user
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Dict


router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


# -------------------View if admin else dont give permission-------------
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


@router.get("/view_user_project_as_admin", tags=["Task"])
async def view_user_project_as_admin(
    user_project: Dict = Depends(get_admin_user),
):
    return user_project


# --------------------------------------------------------------------------

# ------ view the user profile----------------------------------------------
def get_user_project(
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
    view_user_project = crud.return_user(db, username=token_data.username)
    if view_user_project is None:
        raise credentials_exception
    return view_user_project


@router.get("/view_user_project_as_user", tags=["Task"])
async def view_user_project_as_user(
    user_project: Dict = Depends(get_user_project),
):
    return user_project


# ---------------------------------------------------------------------------


@router.post("/create_task", tags=["Task"])
async def create_task(
    task: Create_task,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_user),
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
        return {"Error": "User is not Admin"}
    crud.create_task_for_user(db, task)
