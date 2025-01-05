from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin

from src.app.config import config
from src.app.server.builder import ApplicationConfigurator


alchemy = SQLAlchemyPlugin(
    config=config.alchemy,
)
app_config = ApplicationConfigurator()
