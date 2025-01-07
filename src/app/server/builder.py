from __future__ import annotations
from typing import TYPE_CHECKING

from litestar.plugins import InitPluginProtocol, CLIPluginProtocol

if TYPE_CHECKING:
    from click import Group
    from litestar.config.app import AppConfig


class ApplicationConfigurator(InitPluginProtocol, CLIPluginProtocol):

    def __init__(self) -> None:
        """Initialize ``ApplicationConfigurator``."""

    # def on_cli_init(self, cli: Group) -> None:
    #
    #     from src.app.config.base import get_settings
    #
    #     settings = get_settings()
        # cli.add_command(user_management_app)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Configure application for use with SQLAlchemy.

        Args:
            app_config: The :class:`AppConfig <.config.app.AppConfig>` instance.
        """

        # from src.app.config.base import get_settings

        # from src.app.lib.exceptions import ApplicationError, exception_to_http_response

        # from litestar.security.jwt import Token
        # settings = get_settings()
        # app_config.signature_namespace.update(
        #     {
        #         "Token": Token,
        #     }
        # )
        # app_config.exception_handlers = {
        #     ApplicationError: exception_to_http_response,
        #     RepositoryError: exception_to_http_response,
        # }
        return app_config
