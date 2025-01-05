from litestar import Router

from domain.equipment.controller import EquipmentController
from domain.document.controller import DocumentController
from domain.reference_book.department.controller import DepartmentController
from domain.reference_book.employee.controller import EmployeeController
from domain.reference_book.equipment_name.controller import EquipmentNameController
from domain.web.controller import WebIndexController, WebEquipmentController


def create_api_router() -> Router:
    return Router(
        path="/api",
        route_handlers=[
            EquipmentController,
            DocumentController,
            DepartmentController,
            EmployeeController,
            EquipmentNameController,
        ],
    )


def create_web_router() -> Router:
    return Router(
        route_handlers=[
            WebIndexController,
            WebEquipmentController,
        ],
    )


def get_routers() -> list[Router]:
    return [
        create_web_router(),
        create_api_router(),
    ]
