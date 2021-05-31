from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sql_connect = "mysql://root:@localhost/security"

engine = create_engine(sql_connect)
LocalSession = sessionmaker(bind=engine)
Base = declarative_base()
