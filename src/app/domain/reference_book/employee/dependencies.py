from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.reference_book.employee.service import EmployeeService


async def provide_employee_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[EmployeeService, None]:
    async with EmployeeService.new(db_session) as service:
        yield service
