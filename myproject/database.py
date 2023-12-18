from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlitedb/sqlitedata.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

# Create a session for the database and store it in a variable
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Connect to the database and store it in a variable
Base = declarative_base()
