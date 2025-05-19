"""
Repositorio concreto para la entidad User usando SQLAlchemy async.
Convierte explícitamente entre el modelo ORM (UserModel) y la entidad
de dominio pura (User) para mantener aisladas las capas.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.modules.users.domain.user import User
from app.modules.users.infrastructure.models import User as UserModel
from app.modules.users.interfaces.user_repository import UserRepositoryInterface


# ───────────────────────────── Helpers ──────────────────────────────
def _model_to_entity(model: UserModel) -> User:
    """Convierte un modelo SQLAlchemy en una entidad de dominio."""
    return User(
        id=model.id,
        names=model.names,
        lastnames=model.lastnames,
        email=model.email,
        role_id=model.role_id,
        area_id=model.area_id,
        auth_id=model.auth_id,
    )


# ─────────────────────────── Repositorio ────────────────────────────
class UserRepository(UserRepositoryInterface):
    """Implementación de UserRepositoryInterface con SQLAlchemy (async)."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ──────── Lectura ───────────────────────────────────────────────
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalars().first()
        return _model_to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalars().first()
        return _model_to_entity(model) if model else None

    async def get_by_auth_id(self, auth_id: UUID) -> Optional[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.auth_id == auth_id)
        )
        model = result.scalars().first()
        return _model_to_entity(model) if model else None

    # ──────── Escritura ─────────────────────────────────────────────
    async def create(self, user: User) -> User:
        model = UserModel(**user.__dict__)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return _model_to_entity(model)

    async def update(self, user: User) -> User:
        await self.db.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(**user.__dict__)
        )
        await self.db.commit()
        return await self.get_by_id(user.id)

    async def delete(self, user_id: UUID) -> bool:
        result = await self.db.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    # ──────── Listados ──────────────────────────────────────────────
    async def get_users_by_role(self, role_id: UUID) -> List[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.role_id == role_id)
        )
        return [_model_to_entity(m) for m in result.scalars().all()]

    async def get_users_by_area(self, area_id: UUID) -> List[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.area_id == area_id)
        )
        return [_model_to_entity(m) for m in result.scalars().all()]
