from sqlalchemy.sql.sqltypes import Date, Float, Integer, VARCHAR
from .database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey

# ----------------------login ORM table-------------------------------
class Login(Base):
    __tablename__ = "login"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False)
    password = Column(String(250), nullable=False)
    status = Column(Boolean, nullable=False)
    super_user = Column(Boolean, nullable=False)


# --------------------------------------------------------------------
# -----------------------Project ORM table-----------------------------
class Project(Base):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(20), primary_key=True, index=True)
    date_of_completion = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    description_of_project = Column(VARCHAR(400))


# ---------------------------------------------------------------------

# -------------------Task ORM table-------------------------------------
class Task(Base):
    __tablename__ = "task"

    Task_id = Column(Integer, primary_key=True, index=True)
    Task_name = Column(String(20), nullable=False)
    project_name = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    description = Column(String(400))
    project_created_by = Column(Integer, ForeignKey("login.user_id"), nullable=False)
    project_assigned_to = Column(Integer, ForeignKey("login.user_id"), nullable=False)
    progress = Column(String(50))


# ------------------------------------------------------------------------
