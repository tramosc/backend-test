from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

# Crear la base para los modelos declarativos
Base = declarative_base()

url = settings.database_url
if not url.startswith("postgresql+asyncpg://"):
    url = url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    url,  # Usar la URL modificada
    echo=True,
    future=True
)
# Crear la clase de sesión
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Función para obtener una sesión de base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise