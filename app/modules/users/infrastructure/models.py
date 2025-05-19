from typing import List, Optional
from uuid import UUID as PyUUID
from sqlalchemy import ARRAY, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from app.db.base import Base

class Role(Base):
    __tablename__ = "user_role"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    permissions: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)


class Area(Base):
    __tablename__ = "user_area"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=True)


class User(Base):
    __tablename__ = "user_user"
    
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    names: Mapped[str] = mapped_column(String(100), nullable=False)
    lastnames: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("user_role.id"), nullable=True)
    area_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("user_area.id"), nullable=True)
    card_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("user_area.id"), nullable=True)
    
    # Relaciones
    role: Mapped["Role"] = relationship(foreign_keys=[role_id], uselist=False)
    area: Mapped["Area"] = relationship(foreign_keys=[area_id], uselist=False)
