"""
DTOs / Schemas para entrada‑salida (FastAPI, validaciones, docs).

  Estos modelos **sí** dependen de Pydantic y se usan exclusivamente en adaptadores externos (HTTP, CLI, etc.).
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# ── User Schemas ──────────────────────────────────────────────────
class UserBase(BaseModel):
    names: str
    lastnames: str
    email: EmailStr
    role_id: UUID
    area_id: UUID


class UserCreate(UserBase):
    auth_id: UUID


class UserUpdate(UserBase):
    pass


class UserResponse(BaseModel):
    id: UUID
    names: str
    lastnames: str
    email: str
    auth_id: UUID
    role_id: UUID
    area_id: UUID

    class Config:
        from_attributes = True  # ← permite .model_validate_from_orm


class UserSchema(BaseModel):
    id: str
    names: str
    lastnames: str
    email: str

    class Config:
        orm_mode = True


# ── Role Schemas ──────────────────────────────────────────────────
class RoleBase(BaseModel):
    nombre: str
    permissions: Optional[List[str]] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    nombre: Optional[str] = None
    permissions: Optional[List[str]] = None


class RoleResponse(RoleBase):
    id: UUID

    class Config:
        from_attributes = True


# ── Area Schemas ──────────────────────────────────────────────────
class AreaBase(BaseModel):
    nombre: str
    color: Optional[str] = None


class AreaCreate(AreaBase):
    pass


class AreaUpdate(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None


class AreaResponse(AreaBase):
    id: UUID

    class Config:
        from_attributes = True
