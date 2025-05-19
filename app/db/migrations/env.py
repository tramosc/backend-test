import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Extiende el path para que pueda importar desde app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# Importaciones locales
from app.core.settings import settings
from app.db.base import Base
from app.modules.users.infrastructure.models import User, Role, Area


# Configuración de Alembic
config = context.config

# Configura logging desde alembic.ini
fileConfig(config.config_file_name)

# Sobrescribe sqlalchemy.url con el valor de settings
sync_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
config.set_main_option("sqlalchemy.url", sync_url)

# Define metadata objetivo para autogeneración
target_metadata = Base.metadata


# ✅ FILTRO PARA INCLUIR SOLO CIERTAS TABLAS (en este caso "amenity")
# def include_object(object, name, type_, reflected, compare_to):
#     if type_ == "table":
#         return name == "amenity"
#     return True


# 🧪 MIGRACIONES OFFLINE (genera SQL pero no ejecuta en la base)
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 🚀 MIGRACIONES ONLINE (directamente en la DB)
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# 🚦 Ejecuta según modo (script vs DB directa)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
