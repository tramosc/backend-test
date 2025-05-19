# app/modules/users/application/user_service.py
import logging
from typing import List, Optional, Dict
from uuid import UUID, uuid4

from app.modules.users.interfaces.user_repository import UserRepositoryInterface
from app.modules.users.domain.user import User
from app.modules.users.interfaces.schemas import (
    UserCreate,
    UserUpdate,
)
logger = logging.getLogger(__name__)


class UserService:
    """Casos de uso relacionados con usuarios."""

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    # ──────────────────────────── Consultas ────────────────────────────
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        logger.info("Obteniendo usuario con ID: %s", user_id)
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        logger.info("Buscando usuario con email: %s", email)
        return await self.user_repository.get_by_email(email)

    async def get_user_by_auth_id(self, auth_id: UUID) -> Optional[User]:
        logger.info("Buscando usuario con auth_id: %s", auth_id)
        return await self.user_repository.get_by_auth_id(auth_id)

    # ──────────────────────────── Creación ─────────────────────────────
    async def create_user(self, user_data: UserCreate) -> User:
        email = user_data.email
        logger.info("Creando nuevo usuario con email: %s", email)

        # ¿Existe ya un usuario con ese email?
        if await self.user_repository.get_by_email(email):
            logger.warning("Email duplicado: %s", email)
            raise ValueError("Ya existe un usuario con este email")

        # Construimos la entidad de dominio
        user = User(
            id=uuid4(),
            names=user_data.names,
            lastnames=user_data.lastnames,
            email=email,
            role_id=user_data.role_id,
            area_id=user_data.area_id,
            auth_id=user_data.auth_id,
        )

        return await self.user_repository.create(user)
    # ──────────────────────────── Actualización ────────────────────────
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        logger.info("Actualizando usuario con ID: %s", user_id)

        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            logger.warning("Usuario inexistente: %s", user_id)
            raise ValueError("El usuario no existe")

        # Validar email duplicado
        if user_data.email and user_data.email != existing_user.email:
            dup = await self.user_repository.get_by_email(user_data.email)
            if dup and dup.id != user_id:
                logger.warning("Email ya en uso: %s", user_data.email)
                raise ValueError("El email ya está en uso por otro usuario")
            existing_user.change_email(user_data.email)

        # Actualizar otros campos
        if user_data.names:
            existing_user.names = user_data.names
        if user_data.lastnames:
            existing_user.lastnames = user_data.lastnames
        if user_data.role_id:
            existing_user.role_id = user_data.role_id
        if user_data.area_id:
            existing_user.area_id = user_data.area_id

        return await self.user_repository.update(existing_user)
    # ──────────────────────────── Eliminación ──────────────────────────
    async def delete_user(self, user_id: UUID) -> bool:
        logger.info("Eliminando usuario con ID: %s", user_id)

        if not await self.user_repository.get_by_id(user_id):
            logger.warning("Usuario inexistente: %s", user_id)
            raise ValueError("El usuario no existe")

        return await self.user_repository.delete(user_id)

    # ──────────────────────────── Listados ─────────────────────────────
    async def get_users_by_role(self, role_id: UUID) -> List[User]:
        logger.info("Listando usuarios por rol: %s", role_id)
        return await self.user_repository.get_users_by_role(role_id)

    async def get_users_by_area(self, area_id: UUID) -> List[User]:
        logger.info("Listando usuarios por área: %s", area_id)
        return await self.user_repository.get_users_by_area(area_id)
