
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from app.core.config import settings

# асинхронный движок для работы с бд
engine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,
    future=True
)

# фабрика для создания сессий БД
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# базовый класс для всех моделей ORM
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# получение сессий бд, автоматически закрывает соединение после использования