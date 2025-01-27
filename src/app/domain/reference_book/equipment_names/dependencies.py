from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.reference_book.equipment_names.service import EquipmentNameService


async def provide_item_name_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[EquipmentNameService, None]:
    async with EquipmentNameService.new(db_session) as service:
        yield service
