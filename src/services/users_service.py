from datetime import datetime
import logging
import unittest
from typing import List, Optional
from uuid import UUID, uuid4

from src.models.user import User, UserPost, UserPut
from src.services.users_storage import UserStorage

class UserService(UserStorage):
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
            cls._instance.users = []  # In-memory storage
            cls.initialize_test_data(cls._instance)
        return cls._instance

    def create_user(self, user: UserPost) -> User:
        self.users.append(User(**user.model_dump()))
        return user

    def get_users(self) -> List[User]:
        return self.users

    def get_user(self, user_id: UUID) -> Optional[User]:
        return next((user for user in self.users if user.id == user_id), None)

    def update_user(self, user_id: UUID, updated_user: UserPut) -> Optional[User]:
        logging.info(f"Updating user with ID: {user_id}")
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                logging.info(f"Found user: {user.email}")
                if updated_user.email: self.users[idx].email=updated_user.email
                if updated_user.isdisabled:
                    self.users[idx].isdisabled=updated_user.isdisabled
                    self.users[idx].disabled_at=datetime.today()
                return self.users[idx]
        return None

    def delete_user(self, user_id: UUID) -> bool:
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[idx]
                return True
        return False
    
    def initialize_test_data(self):
        test_users = [
            User(email="test@example.com"),
            User(email="test2@example.com")
        ]
        
        for user in test_users:
            self.create_user(user)
            logging.info(f"Test user added: {user.email} (ID: {user.id})")
