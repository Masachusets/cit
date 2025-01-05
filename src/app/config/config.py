from advanced_alchemy.extensions.litestar import (
    SQLAlchemyAsyncConfig,
    AlembicAsyncConfig,
    AsyncSessionConfig,
    async_autocommit_before_send_handler,
)

from .base import get_settings

settings = get_settings()

alchemy = SQLAlchemyAsyncConfig(
    engine_instance=settings.db.get_engine(),
    before_send_handler=async_autocommit_before_send_handler,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    alembic_config=AlembicAsyncConfig(
        version_table_name=settings.db.MIGRATION_DDL_VERSION_TABLE,
        script_config=settings.db.MIGRATIONS_CONFIG,
        script_location=settings.db.MIGRATION_PATH,
    ),
)
