from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --mysql connection from database of phpmyadmin
# database name = security----------------------
sql_connect = "mysql://root:@localhost/security"

# --------databse engine is created ------------
engine = create_engine(sql_connect)
# ----------------------------------------------

# -----instance of session is created -----------
# for this engine--------------------------------
LocalSession = sessionmaker(bind=engine)

# ------------------------------------------------

# -------base for creating ORM tables -------------
Base = declarative_base()
# -------------------------------------------------
