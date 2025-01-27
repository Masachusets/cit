from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.app.domain.reference_book.department.repository import DepartmentRepository
from src.app.database.models.reference_book.departments import Department

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class DepartmentService(SQLAlchemyAsyncRepositoryService[Department]):
    repository_type: SQLAlchemyAsyncRepository = DepartmentRepository  # type: ignore
    match_fields = ["slug", "name", "type"]
