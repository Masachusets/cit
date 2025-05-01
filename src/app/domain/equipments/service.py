from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from litestar.datastructures.multi_dicts import FormMultiDict
from sqlalchemy import select, func

from .repository import EquipmentRepository, Equipment

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
    from .dto import EquipmentCreateDTO


class EquipmentService(SQLAlchemyAsyncRepositoryService[Equipment]):
    repository_type: SQLAlchemyAsyncRepository = EquipmentRepository  # type: ignore
    # match_fields = [
    #     "it",
    #     "serial_number",
    #     "name_id",
    #     "model",
    #     "manufacture_date",
    #     "arrival_date",
    #     "document_in_id",
    #     "document_out_id",
    #     "status",
    #     "form_number",
    #     "department_id",
    #     "consignment_number",
    #     "employee_id",
    #     "location",
    #     "notes",
    # ]

    @staticmethod
    def clean_assignment_fields(data: dict) -> dict:
        """
        Оставляет только employee_id или только department_id.
        """
        if data.pop("assignment_type", None) == "department":
            data.pop("employee_id", None)
        else:
            data.pop("department_id", None)
            data.pop("consignment_number", None)
        return data 

    async def create_web(self, data: dict, **kwargs) -> Equipment:
        data: dict = self.clean_assignment_fields(data)
        return await super().create(data=data)
    
    async def update_web(self, data: dict, equipment_id: str, **kwargs) -> Equipment:
        data: dict = self.clean_assignment_fields(data)
        return await super().update(data=data, item_id=equipment_id)
    
    async def validate_it_number(self, it: str) -> tuple[bool, str | None]:
        """
        Проверяет валидность и уникальность IT номера
        Returns:
            tuple[valid: bool, error_message: str | None]
        """
        # Проверка формата
        if not it.startswith('it') or not it[2:].isdigit() or len(it) != 7:
            return False, "Неверный формат. Используйте itXXXXX"
        
        # Проверка уникальности
        exists = await self.repository.exists(it=it)
        if exists:
            return False, "Этот инвентарный номер уже используется"
        
        return True, None

    async def generate_next_it(self) -> str:
        """
        Генерирует следующий доступный инвентарный номер
        """
        stmt = select(func.max(Equipment.it))
        result = await self.repository.get(stmt)
        max_it = result.it

        if not max_it:
            return "it00000"
        
        # Извлекаем числовую часть и увеличиваем на 1
        num = int(max_it[2:]) + 1
        return f"it{num:05d}"  # форматируем как 5 цифр с ведущими нулями
