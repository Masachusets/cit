from litestar import Router

from src.app.domain.equipments.controllers import EquipmentController
from src.app.domain.documents.controller import DocumentController
from src.app.domain.reference_book.department.controller import DepartmentController
from src.app.domain.reference_book.employee.controller import EmployeeController
from src.app.domain.reference_book.equipment_names.controller import EquipmentNameController
# from src.app.domain.web.controller import WebIndexController, WebEquipmentController


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


# def create_web_router() -> Router:
#     return Router(
#         route_handlers=[
#             WebIndexController,
#             WebEquipmentController,
#         ],
#     )


def get_routers() -> list[Router]:
    return [
        # create_web_router(),
        create_api_router(),
    ]
