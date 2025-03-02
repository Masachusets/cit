from litestar import Controller, get
from litestar.response import Template


class MainPageController(Controller):
    path = "/index"

    @get(
        path="",
        operation_id="GetMainPage",
        name="main_page:get",
        summary="Main Page",
        description="Render the main page of the application",
    )
    async def get_main_page(self) -> Template:
        """Render the main page."""
        return Template(template_name="pages/main_page.html")
