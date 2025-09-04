from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.models.user import User, UserPost, UserPut
from src.services.users_storage import UserStorage
from src.dependencies import get_user_storage

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_users(service: UserStorage = Depends(get_user_storage)):
    return service.get_users()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID, service: UserStorage = Depends(get_user_storage)):
    user = service.get_user(user_id)
    if not user:
        logger.error("User with id %s not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=User)
def create_user(user: UserPost, service: UserStorage = Depends(get_user_storage)):
    return service.create_user(user)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, updated_user: UserPut, service: UserStorage = Depends(get_user_storage)):
    user = service.update_user(user_id, updated_user);
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user;

@router.delete("/users/{user_id}")
def delete_user(user_id: UUID, service: UserStorage = Depends(get_user_storage)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}



