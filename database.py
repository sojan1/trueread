from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.orm import sessionmaker
from enum import Enum  # Import Enum from Python's standard library
from models import Base, User  # Import Base and User from the new models file

# Database connection settings
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "dbpassword")
#DB_HOST = os.getenv("DB_HOST", "localhost")
#dbhost should be db for it to work on docker
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "isaid")

#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the synchronous engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()

# class UserStatus(Enum):
#     INACTIVE = 0
#     ACTIVE = 1
#     SUSPENDED = 2


# # Define the User model
# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
#     name = Column(String)
#     phone = Column(String)
#     did = Column(String, unique=True, nullable=True)  
#     didverified = Column(Boolean, default=False)
#     status = Column(SQLEnum(UserStatus, native_enum=False), default=UserStatus.ACTIVE)

# # No need for SessionLocal, FastAPI-SQLAlchemy will handle it
# # Create the database tables
# #Base.metadata.create_all(bind=engine)


