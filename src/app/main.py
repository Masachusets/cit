from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig
from litestar.template.config import TemplateConfig

from server.routers import get_routers
from server.plugins import alchemy, app_config


def create_app() -> Litestar:
    from src.app.config.base import get_settings

    settings = get_settings()
    routers = get_routers()
    dependencies = {}

    return Litestar(
        dependencies=dependencies,
        debug=settings.app.DEBUG,
        route_handlers=routers,
        template_config=TemplateConfig(
            directory="templates",
            engine=JinjaTemplateEngine(),
        ),
        static_files_config=[StaticFilesConfig(directories=["static"], path="/static")],
        plugins=[alchemy, app_config],
    )


app = create_app()
