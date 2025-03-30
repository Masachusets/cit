from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .repository import EquipmentRepository, Equipment

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class EquipmentService(SQLAlchemyAsyncRepositoryService[Equipment]):
    repository_type: SQLAlchemyAsyncRepository = EquipmentRepository  # type: ignore
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
        year, month = map(int, data["date_of_manufacture"].split("-"))
        data["year_of_manufacture"] = year
        data["month_of_manufacture"] = month
        del data["date_of_manufacture"]

        return await super().create(data=data)
    
    async def validate_it_number(self, it: str) -> tuple[bool, str | None]:
        """
        Проверяет валидность и уникальность IT номера
        Returns:
            tuple[valid: bool, error_message: str | None]
        """
        # Проверка формата
        if not it.startswith('IT') or not it[2:].isdigit() or len(it) != 7:
            return False, "Неверный формат. Используйте ITXXXXX"
        
        # Проверка уникальности
        exists = await self.repository.exists(it=it)
        if exists:
            return False, "Этот IT номер уже используется"
        
        return True, None

    async def generate_next_it(self) -> str:
        """
        Генерирует следующий доступный IT номер
        """
        result = await self.repository.max(Equipment.it)
        max_it = result.scalar_one_or_none()
        
        if not max_it:
            return "IT00000"
        
        # Извлекаем числовую часть и увеличиваем на 1
        num = int(max_it[2:]) + 1
        return f"IT{num:05d}"  # форматируем как 5 цифр с ведущими нулями
