from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.app.database.models import Equipment

from .repository import EquipmentRepository

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
    from litestar.dto import DTOData


class EquipmentService(SQLAlchemyAsyncRepositoryService[Equipment]):

    repository_type: SQLAlchemyAsyncRepository = EquipmentRepository
    match_fields = [
        "it",
        "serial_number",
        "item_name_id",
        "item_model",
        "year_of_manufacture",
        "month_of_manufacture",
        "date_of_arrival",
        "document_in_id",
        "document_out_id",
        "status",
        "number_of_form",
        "department_slug",
        "employee_slug",
        "number_of_consignment",
        "location",
        "comment",
    ]

    async def create_web(self, data: dict, **kwargs) -> Equipment:
        # Преобразование date_of_manufacture в year_of_manufacture и month_of_manufacture
        year, month = map(int, data['date_of_manufacture'].split('-'))
        data['year_of_manufacture'] = year
        data['month_of_manufacture'] = month
        del data['date_of_manufacture']

        return await super().create(data=data)
