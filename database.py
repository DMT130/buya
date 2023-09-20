from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
db_user = 'postgres'
db_password = 'dercio'
db_host = 'localhost'
db_port=5432
db_name='buya'
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:DMt1m4n3@35.202.150.110:5432/postgres"
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
#SQLALCHEMY_DATABASE_URL="sqlite:///buya.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
