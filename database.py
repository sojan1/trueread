from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.orm import sessionmaker
from enum import Enum  # Import Enum from Python's standard library
from models import Base, User  #, tblWallet  # Import Base and User from the new models file
from config import config

DATABASE_URL = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

# Create the synchronous engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    async with SessionLocal() as session:
        yield session