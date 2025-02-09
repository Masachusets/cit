from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .service import EquipmentService


async def provide_equipment_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[EquipmentService, None]:
    async with EquipmentService.new(db_session) as service:
        yield service
