from datetime import datetime
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from src.services.users_storage import UserStorage
from src.db.entities import AccountTable, UserTable
from src.models.user import User, UserPost, UserPut

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d

class UserRepository(UserStorage):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserPost) -> User:
        row = UserTable(**user.model_dump(exclude={"username"}))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        
        row2 = AccountTable(userid=row.id, username=user.username)
        self.db.add(row2)
        self.db.commit()
        self.db.refresh(row2)
        return User(**row2dict(row))
    
    def get_user(self, user_id: uuid.UUID) -> Optional[User]:
        row = self.db.query(UserTable).filter(UserTable.id == user_id).first()
        return User(**row2dict(row)) if row else None;
    
    def get_users(self) -> List[User]:
        users = self.db.query(UserTable).all()
        return [ User(**row2dict(u)) for u in users ]
    
    def update_user(self, user_id: uuid.UUID, updated_user: UserPut) -> Optional[User]:
        row = self.db.query(UserTable).filter(UserTable.id == user_id).first()
        if row:
            if updated_user.email: row.email = updated_user.email
            if updated_user.isdisabled:
                row.isdisabled = updated_user.isdisabled
                row.disabled_at = datetime.today()
            
            self.db.commit()
            self.db.refresh(row)
            return User(**row2dict(row))
        return None

    def delete_user(self, user_id: uuid.UUID) -> bool:
        row = self.db.query(UserTable).filter(UserTable.id == user_id).first()
        if row:
            self.db.delete(row)
            self.db.commit()
            return True
        return False