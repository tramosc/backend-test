import re
import uuid
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.sql import func

# Tu antiguo Base sigue igual para la conexión (no tocar):
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class ORMBase(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

class ORMBaseModel(ORMBase):
    __abstract__ = True

    id: Mapped[PyUUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String(250), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)
