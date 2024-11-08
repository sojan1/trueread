# models.py
import uuid
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID

# Define the base class for SQLAlchemy models
Base = declarative_base()

class UserStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1
    SUSPENDED = 2

# Define the User model
class User(Base):
    __tablename__ = "users"
    
    #id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    displayname = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    did = Column(String, unique=True, nullable=True)  
    didverified = Column(Boolean, default=False)
    status = Column(SQLEnum(UserStatus, native_enum=False), default=UserStatus.ACTIVE)
