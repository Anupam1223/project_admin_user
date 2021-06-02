from sqlalchemy.orm import Session
from initialize import models
from . import schema
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --------------------password related task------------------------------------
def get_password_hash(password):
    """
    takes in plain password and returns hashed password
    """
    return pwd_context.hash(password)


def check_password(password, hash_password) -> str:
    """
    takes in plain password and hashed password,
    returns true if matched else return false
    """
    return pwd_context.verify(password, hash_password)


# -----------------Reading user from database----------------------------------
def read_user(db: Session, username):
    """
    takes in session and username,
    returns record which is matched to this username
    """
    return db.query(models.Login).filter(models.Login.username == username).first()


# -----------------------------------------------------------------------------

# -----Storing user in database------------------------------------------------
def create_user(db: Session, create: schema.CreateUser):
    """
    Takes in session and CreateUser schema from schema model and
    insert the values brought by this model in our databse table "login"
    """
    hashed_password = get_password_hash(create.password)
    db_user = models.Login(
        user_id=create.user_id,
        first_name=create.first_name,
        last_name=create.last_name,
        username=create.username,
        email=create.email,
        password=hashed_password,
        status=create.status,
        super_user=create.super_user,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ----------------------------------------------------------------------------
def pass_user(db: Session, username):
    user_value = (
        db.query(models.Login).filter(models.Login.username == username).first()
    )
    status = user_value.status
    if status == True:
        user_dict = jsonable_encoder(user_value)
        current_user = schema.User(**user_dict)
        return current_user
    return None


# -----------------------------------------------------------------------------
