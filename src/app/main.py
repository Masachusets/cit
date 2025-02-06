from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig


def create_app() -> Litestar:
    from .server.routers import get_routers
    from .server.plugins import alchemy, app_config
    from .config.base import get_settings

    settings = get_settings()
    routers = get_routers()
    dependencies = {}

    return Litestar(
        dependencies=dependencies,
        debug=settings.app.DEBUG,
        route_handlers=routers,
        plugins=[alchemy, app_config],
        template_config=TemplateConfig(
            directory="src/app/templates",
            engine=JinjaTemplateEngine,
        ),
    )


app = create_app()
