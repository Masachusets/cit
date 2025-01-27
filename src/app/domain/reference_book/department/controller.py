from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from litestar import Controller, get, post, delete, patch
from litestar.di import Provide
from litestar.response import Template

from src.app.domain.reference_book.department import urls
from src.app.domain.reference_book.department.dependencies import (
    provide_department_service,
)
from src.app.domain.reference_book.department.dto import (
    DepartmentReadCreateDTO,
    DepartmentUpdateDTO,
)
from src.app.domain.reference_book.department.service import DepartmentService
from src.app.database.models.reference_book.departments import Department

if TYPE_CHECKING:
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Parameter


class DepartmentController(Controller):
    dependencies = {"service": Provide(provide_department_service)}
    tags = ["Department"]
    return_dto = DepartmentReadCreateDTO

    @get(
        path=urls.DEPARTMENT_LIST,
        operation_id="ListDepartments",
        name="departments:list",
        summary="Get list of departments",
        description="Get list of departments",
    )
    async def get_list(
        self,
        service: DepartmentService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Department]:
        """Get list of departments"""
        results, total = await service.list_and_count()  # (*filters)
        return service.to_schema(
            data=results,
            total=total,
            # filters=filters,
        )

    @get(
        path=urls.DEPARTMENT_DETAIL,
        operation_id="GetDepartment",
        name="departments:get",
        summary="Get department",
        description="Retrieve the details of a department",
    )
    async def get_department(
        self,
        service: DepartmentService,
        department_slug: Annotated[
            str,
            Parameter(
                title="Department slug",
                description="The slug of the department to retrieve",
            ),
        ],
    ) -> Department:
        """Retrieve the details of a department."""
        db_obj = await service.get(department_slug)
        return service.to_schema(db_obj)

    @post(
        path=urls.DEPARTMENT_CREATE,
        operation_id="CreateDepartment",
        name="departments:create",
        summary="Create department",
        description="Create a new department",
        # guards=[],
        cache_control=None,
        dto=DepartmentReadCreateDTO,
    )
    async def create_department(
        self,
        service: DepartmentService,
        data: DTOData[Department],
    ) -> Department:
        """Create a new department"""
        db_obj = await service.create(data.create_instance())
        return service.to_schema(db_obj)

    @patch(
        path=urls.DEPARTMENT_UPDATE,
        operation_id="UpdateDepartment",
        name="departments:update",
        summary="Update a department",
        description="Update the details of a department",
        # guards=[],
        dto=DepartmentUpdateDTO,
    )
    async def update_department(
        self,
        service: DepartmentService,
        data: DTOData[Department],
        department_slug: Annotated[
            str,
            Parameter(
                title="Department slug",
                description="The slug of the department to update",
            ),
        ],
    ) -> Department:
        """Update a department"""
        db_obj = await service.update(
            item_id=department_slug,
            data=data.create_instance(),
        )
        return service.to_schema(db_obj)

    @delete(
        path=urls.DEPARTMENT_DELETE,
        operation_id="DeleteDepartment",
        name="departments:delete",
        summary="Delete department",
        description="Delete a department",
        # guards=[],
        return_dto=None,
    )
    async def delete_department(
        self,
        service: DepartmentService,
        department_slug: Annotated[
            str,
            Parameter(
                title="Department ID",
                description="The ID of the department to delete",
            ),
        ],
    ) -> None:
        """Delete a department"""
        await service.delete(department_slug)

    @get(
        path=urls.DEPARTMENT_LIST_WEB,
        operation_id="Web:ListDepartments",
        name="departments:list_web",
        summary="Get list of departments",
        description="Get list of departments for template",
        include_in_schema=False,
    )
    async def get_list_web(
        self,
        service: DepartmentService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> Template:
        """Get list of departments for template"""
        results, total = await service.list_and_count()  # (*filters)
        template_name = "reference_book/departments.html"
        return Template(
            template_name=template_name,
            context={"departments": results, "total": total},
        )
