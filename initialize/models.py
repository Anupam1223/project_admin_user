from sqlalchemy.sql.sqltypes import Date, Float, VARCHAR
from .database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey


class Login(Base):
    __tablename__ = "login"

    first_name = Column(String(20), primary_key=True, index=True)
    last_name = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False)
    password = Column(String(250), nullable=False)
    status = Column(Boolean, nullable=False)
    super_user = Column(Boolean, nullable=False)


class Project(Base):
    __tablename__ = "project"

    project_name = Column(String(20), primary_key=True, index=True)
    date_of_completion = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    description_of_project = Column(VARCHAR(400))
    progress = Column(VARCHAR(10))


class Task(Base):
    __tablename__ = "task"

    Task_name = Column(String(20), primary_key=True, index=True)
    project_name = Column(
        String(20), ForeignKey("project.project_name"), nullable=False
    )
    description = Column(VARCHAR(400))
    project_created_by = Column(
        String(20), ForeignKey("login.first_name"), nullable=False
    )
    project_assigned_to = Column(
        String(20), ForeignKey("login.first_name"), nullable=False
    )
