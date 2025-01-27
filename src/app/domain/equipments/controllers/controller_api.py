from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from litestar import Controller, get, post, delete, patch
from litestar.di import Provide

from .. import urls
from ..dependencies import provide_item_service
from ..dto import EquipmentReadDTO, EquipmentCreateDTO, EquipmentUpdateDTO
from ..service import EquipmentService
from src.app.database.models import Equipment

if TYPE_CHECKING:
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Parameter


class EquipmentController(Controller):
    dependencies = {"service": Provide(provide_item_service)}
    tags = ["Equipment"]
    return_dto = EquipmentReadDTO

    @get(
        path=urls.ITEM_LIST,
        operation_id="ListEquipments",
        name="items:list",
        summary="List of items",
        description="Get list of items",
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
        path=urls.ITEM_DETAIL,
        operation_id="GetEquipment",
        name="items:get",
        summary="Get item",
        description="Retrieve the details of a item",
    )
    async def get_item(
        self,
        service: EquipmentService,
        item_it: Annotated[
            str,
            Parameter(
                title="Equipment ID",
                description="The ID of the item to retrieve",
            ),
        ],
    ) -> Equipment:
        """Retrieve the details of a item."""
        db_obj = await service.get(item_it)
        return service.to_schema(db_obj)

    @post(
        path=urls.ITEM_CREATE,
        operation_id="CreateEquipment",
        name="items:create",
        summary="Create item",
        description="Create a new item",
        # guards=[],
        cache_control=None,
        dto=EquipmentCreateDTO,
    )
    async def create_item(
        self,
        service: EquipmentService,
        data: DTOData[Equipment],
    ) -> Equipment:
        """Create a new item"""
        db_obj = await service.create(data.create_instance())
        return service.to_schema(db_obj)

    @patch(
        path=urls.ITEM_UPDATE,
        operation_id="UpdateEquipment",
        name="items:update",
        summary="Update a item",
        description="Update the details of a item",
        # guards=[],
        dto=EquipmentUpdateDTO,
    )
    async def update_item(
        self,
        service: EquipmentService,
        data: DTOData[Equipment],
        item_it: Annotated[
            str,
            Parameter(
                title="Equipment IT",
                description="The IT of the item to update",
            ),
        ],
    ) -> Equipment:
        """Update a item"""
        db_obj = await service.update(
            item_id=item_it,
            data=data.create_instance(),
        )
        return service.to_schema(db_obj)

    @delete(
        path=urls.ITEM_DELETE,
        operation_id="DeleteEquipment",
        name="items:delete",
        summary="Delete item",
        description="Delete a item",
        # guards=[],
        return_dto=None,
    )
    async def delete_item(
        self,
        service: EquipmentService,
        item_it: Annotated[
            str,
            Parameter(
                title="Equipment IT",
                description="The IT of the item to delete",
            ),
        ],
    ) -> None:
        """Delete a item"""
        await service.delete(item_it)
