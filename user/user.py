from sqlalchemy import engine
from initialize.database import LocalSession, engine
from initialize import models
from . import schema, crud
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import JWTError, jwt

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------- info regarding token -----------------------------
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# -----------------------------------------------------------------------------
router = APIRouter()


def get_user():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


# ---------------------- Creating token -------------------------------------
def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ----------------------------------------------------------------------------

# ------Add new user in database----------------------------------------------
@router.post("/create_newuser/", response_model=schema.UserResponse, tags=["User"])
def create_newuser(user: schema.CreateUser, db: Session = Depends(get_user)):
    return crud.create_user(db, user)


# ----------------------------------------------------------------------------

# -------Provide token if valid user------------------------------------------
@router.post("/verify_stored_user/", response_model=schema.Token, tags=["User"])
async def login_for_access_token(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_user)
):
    user_value = crud.read_user(db, form.username)
    username = user_value.username
    password = user_value.password
    verify_password = crud.check_password(form.password, password)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ----------Get User Using Authentication----------------------------
def get_current_user(
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
    current_user = crud.pass_user(db, username=token_data.username)
    if current_user is None:
        raise credentials_exception
    return current_user


# ---------Path Operation Function---------------------------------
@router.get("/get_user/", response_model=schema.User, tags=["User"])
def view_user_profile(current_user: schema.User = Depends(get_current_user)):
    return current_user


# --------------------------------------------------------------------------------
