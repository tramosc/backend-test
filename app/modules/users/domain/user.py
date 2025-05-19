
from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    names: str
    lastnames: str
    email: str
    role_id: UUID
    area_id: UUID
    auth_id: UUID | None = None

    # Ejemplo de regla de dominio
    def change_email(self, new_email: str) -> None:
        """Cambia el email aplicando una regla simple de normalización."""
        self.email = new_email.strip().lower()