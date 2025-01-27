from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from litestar import Controller, get, post, delete, patch
from litestar.di import Provide
from litestar.response import Template

from src.app.database.models.reference_book.employees import Employee

from . import urls
from .dependencies import provide_employee_service
from .dto import EmployeeReadDTO, EmployeeCreateDTO, EmployeeUpdateDTO
from .service import EmployeeService

if TYPE_CHECKING:
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Parameter


class EmployeeController(Controller):
    dependencies = {"service": Provide(provide_employee_service)}
    tags = ["Employee"]
    return_dto = EmployeeReadDTO

    @get(
        path=urls.EMPLOYEE_LIST,
        operation_id="ListEmployees",
        name="employees:list",
        summary="Get list of Employees",
        description="Get list of Employees",
    )
    async def get_list(
        self,
        service: EmployeeService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Employee]:
        """Get list of Employees"""
        results, total = await service.list_and_count()  # (*filters)
        return service.to_schema(
            data=results,
            total=total,
            # filters=filters,
        )

    @get(
        path=urls.EMPLOYEE_DETAIL,
        operation_id="GetEmployee",
        name="employees:get",
        summary="Get Employee",
        description="Retrieve the details of a Employee",
    )
    async def get_employee(
        self,
        service: EmployeeService,
        employee_slug: Annotated[
            str,
            Parameter(
                title="employee slug",
                description="The slug of the Employee to retrieve",
            ),
        ],
    ) -> Employee:
        """Retrieve the details of a Employee."""
        db_obj = await service.get(employee_slug)
        return service.to_schema(db_obj)

    @post(
        path=urls.EMPLOYEE_CREATE,
        operation_id="CreateEmployee",
        name="employees:create",
        summary="Create Employee",
        description="Create a new Employee",
        # guards=[],
        cache_control=None,
        dto=EmployeeCreateDTO,
    )
    async def create_employee(
        self,
        service: EmployeeService,
        data: DTOData[Employee],
    ) -> Employee:
        """Create a new Employee"""
        db_obj = await service.create(data.create_instance())
        return service.to_schema(db_obj)

    @patch(
        path=urls.EMPLOYEE_UPDATE,
        operation_id="UpdateEmployee",
        name="employees:update",
        summary="Update a Employee",
        description="Update the details of a Employee",
        # guards=[],
        dto=EmployeeUpdateDTO,
    )
    async def update_employee(
        self,
        service: EmployeeService,
        data: DTOData[Employee],
        employee_slug: Annotated[
            str,
            Parameter(
                title="Employee slug",
                description="The slug of the Employee to update",
            ),
        ],
    ) -> Employee:
        """Update a Employee"""
        db_obj = await service.update(
            item_id=employee_slug,
            data=data.create_instance(),
        )
        return service.to_schema(db_obj)

    @delete(
        path=urls.EMPLOYEE_DELETE,
        operation_id="DeleteEmployee",
        name="employees:delete",
        summary="Delete Employee",
        description="Delete a Employee",
        # guards=[],
        return_dto=None,
    )
    async def delete_employee(
        self,
        service: EmployeeService,
        employee_slug: Annotated[
            str,
            Parameter(
                title="Employee slug",
                description="The slug of the Employee to delete",
            ),
        ],
    ) -> None:
        """Delete a Employee"""
        await service.delete(employee_slug)

    @get(
        path=urls.EMPLOYEE_LIST_WEB,
        operation_id="Web:ListEmployees",
        name="employees:list_web",
        summary="Get list of employees",
        description="Get list of employees for template",
        include_in_schema=False,
    )
    async def get_list_web(
        self,
        service: EmployeeService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> Template:
        """Get list of departments for template"""
        results, total = await service.list_and_count()  # (*filters)
        template_name = "reference_book/employees.html"
        return Template(
            template_name=template_name,
            context={"employees": results, "total": total},
        )
