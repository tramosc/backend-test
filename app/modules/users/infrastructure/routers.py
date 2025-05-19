# app/modules/users/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.modules.users.interfaces.schemas import UserCreate, UserUpdate, UserResponse
from app.modules.users.infrastructure.repository import UserRepository
from app.modules.users.application.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

# Dependencia para obtener repositorio
def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

# Dependencia para obtener servicio, inyectando repositorio
def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),  # <- servicio
):
    # El servicio maneja la lógica
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Detalles para debugging
        import traceback
        print("ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/", response_model=List[UserResponse])
async def read_users_by_role(
    role_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_users_by_role(role_id)
    return users