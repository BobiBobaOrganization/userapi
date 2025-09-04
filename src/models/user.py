from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class User(BaseModel):
    id: UUID = uuid4()
    email: EmailStr = Field(..., max_length=1024)
    isdisabled: bool = False
    created_at: datetime = datetime.today()
    disabled_at: datetime | None = datetime.today() if isdisabled else None
    
class UserPost(BaseModel):
    email: EmailStr = Field(..., max_length=1024)
    username: str = Field(..., min_length=5, max_length=20)

class UserPut(BaseModel):
    email: Optional[EmailStr] = None
    isdisabled: Optional[bool] = False