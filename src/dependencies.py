from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Settings, get_settings
from src.db.users_repository import UserRepository
from src.services.users_service import UserService
from src.services.users_storage import UserStorage

def get_user_storage() -> UserStorage:
    if get_settings().TEST_MODE:
        return UserService() 
    else:
        engine = create_engine(get_settings().DATABASE_URL, echo=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        return UserRepository(db)