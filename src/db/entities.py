import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime, UUID, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from config import get_settings

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"
    __table_args__ = { "schema": get_settings().DATABASE_SCHEMA }  

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    account = relationship("AccountTable", back_populates="user")
    email = Column(String(1024), nullable=False, unique=True, index=True)
    isdisabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.today(), nullable=False)
    disabled_at = Column(DateTime, nullable=True)

class AccountTable(Base):
    __tablename__ = "accounts"
    __table_args__ = {"schema": get_settings().DATABASE_SCHEMA }

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False) 
    userid = Column(UUID(as_uuid=True), ForeignKey(f"{get_settings().DATABASE_SCHEMA}.users.id"), nullable=False, unique=True, index=True)
    user = relationship("UserTable", back_populates="account")
    username = Column(String(20), unique=True, nullable=False, index=True)
    firstname = Column(String(256), nullable=True)
    lastname = Column(String(256), nullable=True)
    sex = Column(String(24), nullable=True)
    phone = Column(String(16), nullable=True)