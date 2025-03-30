from litestar import Controller, get
from litestar.response import Template


class MainPageController(Controller):

    @get(
        path="/",
        operation_id="GetMainPage",
        name="main_page:get",
    )
    async def get_main_page(self) -> Template:
        """Render the main page."""
        return Template(template_name="pages/main_page.html")
