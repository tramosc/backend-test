# app/modules/users/interfaces/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.modules.users.domain.user import User

class UserRepositoryInterface(ABC):
    """
    Interfaz abstracta para el repositorio de usuarios.
    Define los métodos que debe implementar cualquier
    repositorio concreto para usuarios.
    """
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su correo electrónico"""
        pass
    
    @abstractmethod
    async def get_by_auth_id(self, auth_id: UUID) -> Optional[User]:
        """Obtiene un usuario por el ID de autenticación asociado"""
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Elimina un usuario por su ID"""
        pass
    
    @abstractmethod
    async def get_users_by_role(self, role_id: UUID) -> List[User]:
        """Lista usuarios que tienen un rol específico"""
        pass
    
    @abstractmethod
    async def get_users_by_area(self, area_id: UUID) -> List[User]:
        """Lista usuarios que pertenecen a un área específica"""
        pass