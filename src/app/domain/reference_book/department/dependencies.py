from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.reference_book.department.service import DepartmentService


async def provide_department_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[DepartmentService, None]:
    async with DepartmentService.new(db_session) as service:
        yield service
