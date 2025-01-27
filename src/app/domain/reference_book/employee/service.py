from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.app.domain.reference_book.employee.repository import EmployeeRepository
from src.app.database.models.reference_book.employees import Employee

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class EmployeeService(SQLAlchemyAsyncRepositoryService[Employee]):
    repository_type: SQLAlchemyAsyncRepository = EmployeeRepository  # type: ignore
    match_fields = ["slug", "full_name", "card_number"]
