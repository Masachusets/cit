from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from litestar import Controller, get, post, delete, patch
from litestar.di import Provide

from .. import urls
from ..dependencies import provide_equipment_service
from ..dto import EquipmentReadDTO, EquipmentCreateDTO, EquipmentUpdateDTO
from ..service import EquipmentService
from src.app.database.models import Equipment

if TYPE_CHECKING:
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Parameter


class EquipmentController(Controller):
    dependencies = {"service": Provide(provide_equipment_service)}
    tags = ["Equipment"]
    return_dto = EquipmentReadDTO

    @get(
        path=urls.EQUIPMENT_LIST,
        operation_id="ListEquipments",
        name="equipments:list",
        summary="List of equipments",
        description="Get list of equipments",
    )
    async def get_list(
        self,
        service: EquipmentService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Equipment]:
        results, total = await service.list_and_count()  # (*filters)
        return service.to_schema(
            data=results,
            total=total,
            # filters=filters,
        )

    @get(
        path=urls.EQUIPMENT_DETAIL,
        operation_id="GetEquipment",
        name="equipments:get",
        summary="Get equipment",
        description="Retrieve the details of an equipment",
    )
    async def get_equipment(
        self,
        service: EquipmentService,
        equipment_it: Annotated[
            str,
            Parameter(
                title="Equipment ID",
                description="The ID of the item to retrieve",
            ),
        ],
    ) -> Equipment:
        """Retrieve the details of an equipment"""
        db_obj = await service.get(equipment_it)
        return service.to_schema(db_obj)

    @post(
        path=urls.EQUIPMENT_CREATE,
        operation_id="CreateEquipment",
        name="equipments:create",
        summary="Create equipment",
        description="Create a new equipment",
        # guards=[],
        cache_control=None,
        dto=EquipmentCreateDTO,
    )
    async def create_equipment(
        self,
        service: EquipmentService,
        data: DTOData[Equipment],
    ) -> Equipment:
        """Create a new equipment"""
        db_obj = await service.create(data)
        return service.to_schema(db_obj)

    @patch(
        path=urls.EQUIPMENT_UPDATE,
        operation_id="UpdateEquipment",
        name="equipments:update",
        summary="Update an equipment",
        description="Update the details of an equipment",
        # guards=[],
        dto=EquipmentUpdateDTO,
    )
    async def update_equipment(
        self,
        service: EquipmentService,
        data: DTOData[Equipment],
        equipment_it: Annotated[
            str,
            Parameter(
                title="Equipment IT",
                description="The IT of the item to update",
            ),
        ],
    ) -> Equipment:
        """Update an equipment"""
        db_obj = await service.update(
            item_id=equipment_it,
            data=data.create_instance(),
        )
        return service.to_schema(db_obj)

    @delete(
        path=urls.EQUIPMENT_DELETE,
        operation_id="DeleteEquipment",
        name="items:delete",
        summary="Delete equipment",
        description="Delete an equipment",
        # guards=[],
        return_dto=None,
    )
    async def delete_equipment(
        self,
        service: EquipmentService,
        equipment_it: Annotated[
            str,
            Parameter(
                title="Equipment IT",
                description="The IT of the equipment to delete",
            ),
        ],
    ) -> None:
        """Delete an equipment"""
        await service.delete(equipment_it)
