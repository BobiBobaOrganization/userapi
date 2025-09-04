from sqlalchemy import UUID
from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.user import User, UserPost, UserPut

class UserStorage(ABC):
    @abstractmethod
    def create_user(self, user: UserPost) -> User:
        pass
    
    @abstractmethod
    def get_users(self) -> List[User]:
        pass
    
    @abstractmethod
    def get_user(self, user_id: UUID) -> Optional[User]:
        pass
    
    @abstractmethod
    def update_user(self, user_id: UUID, updated_user: UserPut) -> Optional[User]:
        pass
    
    @abstractmethod
    def delete_user(self, user_id: UUID) -> bool:
        pass