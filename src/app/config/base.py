import binascii
import os
from dataclasses import field, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Final, Any

from litestar.serialization import decode_json, encode_json
from litestar.utils.module_loader import module_to_os_path
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool


DEFAULT_MODULE_NAME = "src.app"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)

TRUE_VALUES = {"True", "true", "1", "yes", "Y", "T"}


@dataclass
class DatabaseSettings:
    ECHO: bool = field(
        default_factory=lambda: os.getenv("DB_ECHO", False) in TRUE_VALUES
    )
    ECHO_POOL: bool = field(
        default_factory=lambda: os.getenv("DB_ECHO_POOL", False) in TRUE_VALUES
    )
    POOL_DISABLED: bool = field(
        default_factory=lambda: os.getenv("DB_POOL_DISABLED", False) in TRUE_VALUES
    )
    POOL_MAX_OVERFLOW: int = field(
        default_factory=lambda: int(os.getenv("DB_POOL_MAX_OVERFLOW", "10"))
    )
    POOL_SIZE: int = field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "5")))
    POOL_TIMEOUT: int = field(
        default_factory=lambda: int(os.getenv("DB_POOL_TIMEOUT", "30"))
    )
    POOL_RECYCLE: int = field(
        default_factory=lambda: int(os.getenv("DB_POOL_RECYCLE", "300"))
    )
    POOL_PRE_PING: bool = field(
        default_factory=lambda: os.getenv("DB_POOL_PRE_PING", "False") in TRUE_VALUES
    )
    URL: str = field(
        default_factory=lambda: os.getenv("DB_URL", "sqlite+aiosqlite:///stock.db")
    )
    MIGRATIONS_CONFIG: str = f"{BASE_DIR}/database/migrations/alembic.ini"
    MIGRATION_PATH: str = f"{BASE_DIR}/database/migrations"
    MIGRATION_DDL_VERSION_TABLE: str = "ddl_version"
    FIXTURE_PATH: str = f"{BASE_DIR}/database/fixtures"
    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance
        if self.URL.startswith("postgres+asyncpg"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
                pool_use_lifo=True,
                poolclass=NullPool if self.POOL_DISABLED else None,
            )

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(
                dbapi_connection: Any, _: Any
            ) -> Any:  # pragma: no cover
                """Using msgspec for serialization of the json column values means that the
                output is binary, not `str` like `json.dumps` would output.
                SQLAlchemy expects that the json serializer returns `str` and calls `.encode()` on the value to
                turn it to bytes before writing to the JSONB column. I'd need to either wrap `serialization.to_json` to
                return a `str` so that SQLAlchemy could then convert it to binary, or do the following, which
                changes the behaviour of the dialect to expect a binary value from the serializer.
                See Also
                https://github.com/sqlalchemy/sqlalchemy/blob/14bfbadfdf9260a1c40f63b31641b27fe9de12a0/lib/sqlalchemy/dialects/postgresql/asyncpg.py#L934
                pylint: disable=line-too-long
                """

                def encoder(bin_value: bytes) -> bytes:
                    return b"\x01" + encode_json(bin_value)

                def decoder(bin_value: bytes) -> Any:
                    # the byte is the \x01 prefix for jsonb used by PostgreSQL.
                    # asyncpg returns it when format='binary'
                    return decode_json(bin_value[1:])

                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "jsonb",
                        encoder=encoder,
                        decoder=decoder,
                        schema="pg_catalog",
                        format="binary",
                    ),
                )
                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "json",
                        encoder=encoder,
                        decoder=decoder,
                        schema="pg_catalog",
                        format="binary",
                    ),
                )

        elif self.URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
                poolclass=NullPool if self.POOL_DISABLED else None,
            )
            """Database session factory.

            See [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker].
            """

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(
                dbapi_connection: Any, _: Any
            ) -> Any:  # pragma: no cover
                """Override the default begin statement.  The disables the built in begin execution."""
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "begin")
            def _sqla_on_begin(dbapi_connection: Any) -> Any:  # pragma: no cover
                """Emits a custom begin"""
                dbapi_connection.exec_driver_sql("BEGIN")

        else:
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )
        self._engine_instance = engine
        return self._engine_instance


@dataclass
class ServerSettings:
    APP_LOC: str = field(default_factory=lambda: os.getenv("APP_LOC", "app.main:app"))
    APP_LOC_IS_FACTORY: bool = False
    HOST: str = field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    PORT: int = field(default_factory=lambda: int(os.getenv("PORT", 8000)))
    KEEPALIVE: int = field(default_factory=lambda: int(os.getenv("KEEPALIVE", "65")))
    RELOAD: bool = field(
        default_factory=lambda: os.getenv("USE_RELOAD", "False") in TRUE_VALUES
    )
    RELOAD_DIRS: list[str] = field(
        default_factory=lambda: os.getenv("RELOAD_DIRS", [f"{BASE_DIR}"])
    )
    HTTP_WORKERS: int = field(
        default_factory=lambda: (
            int(os.getenv("WEB_CONCURRENCY"))
            if os.getenv("WEB_CONCURRENCY") is not None
            else None
        )
    )


@dataclass
class AppSettings:
    URL: str = field(
        default_factory=lambda: os.getenv("APP_URL", "http://127.0.0.1:8000")
    )
    DEBUG: bool = field(
        default_factory=lambda: os.getenv("APP_DEBUG", "True") in TRUE_VALUES
    )
    SECRET_KEY: str = field(
        default_factory=lambda: os.getenv(
            "SECRET_KEY",
            binascii.hexlify(os.urandom(32)).decode(encoding="utf-8"),
        )
    )
    NAME: str = field(default_factory=lambda: os.getenv("APP_NAME", "Stocktaking"))


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    server: ServerSettings = field(default_factory=ServerSettings)
    # log: LogSettings = field(default_factory=LogSettings)

    @classmethod
    def from_env(cls, dotenv_path: str = ".env") -> "Settings":
        from litestar.cli._utils import console

        if Path(dotenv_path).is_file():
            from dotenv import load_dotenv

            console.print(
                f"[yellow]Loading environment configuration from {dotenv_path}"
            )

            load_dotenv(dotenv_path)
        return Settings()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.from_env()
