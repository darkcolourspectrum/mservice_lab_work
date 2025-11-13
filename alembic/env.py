# alembic/env.py
# Файл окружения для Alembic миграций

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Импорт настроек и моделей
from app.core.config import settings
from app.db.base import Base

# Конфигурация Alembic
config = context.config

# Установка URL базы данных из настроек приложения
config.set_main_option("sqlalchemy.url", settings.database_url)

# Настройка логирования из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для автогенерации миграций
# Base.metadata содержит информацию обо всех моделях
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций в 'offline' режиме.
    В этом режиме не требуется подключение к БД.
    Генерируется только SQL скрипт.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Выполнение миграций с использованием существующего подключения.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Создание асинхронного движка и выполнение миграций.
    """
    # Конфигурация движка из alembic.ini
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.database_url
    
    # Создание асинхронного движка
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Выполнение миграций в асинхронном контексте
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Запуск миграций в 'online' режиме.
    Требуется реальное подключение к БД.
    """
    import asyncio
    asyncio.run(run_async_migrations())


# Определение режима работы (offline/online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()