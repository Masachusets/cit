from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.app.domain.reference_book.equipment_names.repository import (
    EquipmentNameRepository,
)
from src.app.database.models.reference_book.equipment_names import EquipmentName

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class EquipmentNameService(SQLAlchemyAsyncRepositoryService[EquipmentName]):
    repository_type: SQLAlchemyAsyncRepository = EquipmentNameRepository  # type: ignore
    match_fields = ["id", "name", "nomenclature_code"]
