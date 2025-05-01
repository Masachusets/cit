from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from litestar import Controller, Request, get, post, delete, patch
from litestar.di import Provide
from litestar.response import Template

from src.app.domain.reference_book.equipment_names import urls
from src.app.domain.reference_book.equipment_names.dependencies import (
    provide_item_name_service,
)
from src.app.domain.reference_book.equipment_names.dto import (
    EquipmentNameReadCreateDTO,
    EquipmentNameUpdateDTO,
)
from src.app.domain.reference_book.equipment_names.service import EquipmentNameService
from src.app.database.models.reference_book.equipment_names import EquipmentName

if TYPE_CHECKING:
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Parameter


class EquipmentNameController(Controller):
    dependencies = {"service": Provide(provide_item_name_service)}
    tags = ["EquipmentName"]
    return_dto = EquipmentNameReadCreateDTO

    @get(
        path=urls.ITEM_NAME_LIST,
        operation_id="ListEquipmentNames",
        name="EquipmentNames:list",
        summary="Get list of EquipmentNames",
        description="Get list of EquipmentNames",
    )
    async def get_list(
        self,
        service: EquipmentNameService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[EquipmentName]:
        """Get list of EquipmentNames"""
        results, total = await service.list_and_count()  # (*filters)
        return service.to_schema(
            data=results,
            total=total,
            # filters=filters,
        )

    @get(
        path=urls.ITEM_NAME_DETAIL,
        operation_id="GetEquipmentName",
        name="EquipmentNames:get",
        summary="Get EquipmentName",
        description="Retrieve the details of a EquipmentName",
    )
    async def get_item_name(
        self,
        service: EquipmentNameService,
        id: Annotated[
            int,
            Parameter(
                title="EquipmentName id",
                description="The id of the EquipmentName to retrieve",
            ),
        ],
    ) -> EquipmentName:
        """Retrieve the details of a EquipmentName."""
        db_obj = await service.get(id)
        return service.to_schema(db_obj)

    @post(
        path=urls.ITEM_NAME_CREATE,
        operation_id="CreateEquipmentName",
        name="EquipmentNames:create",
        summary="Create EquipmentName",
        description="Create a new EquipmentName",
        # guards=[],
        cache_control=None,
        dto=EquipmentNameReadCreateDTO,
    )
    async def create_item_name(
        self,
        service: EquipmentNameService,
        data: DTOData[EquipmentName],
    ) -> EquipmentName:
        """Create a new EquipmentName"""
        db_obj = await service.create(data.create_instance())
        return service.to_schema(db_obj)

    @patch(
        path=urls.ITEM_NAME_UPDATE,
        operation_id="UpdateEquipmentName",
        name="EquipmentNames:update",
        summary="Update a EquipmentName",
        description="Update the details of a EquipmentName",
        # guards=[],
        dto=EquipmentNameUpdateDTO,
    )
    async def update_item_name(
        self,
        service: EquipmentNameService,
        data: DTOData[EquipmentName],
        id: Annotated[
            int,
            Parameter(
                title="EquipmentName nomenclature_code",
                description="The nomenclature_code of the EquipmentName to update",
            ),
        ],
    ) -> EquipmentName:
        """Update a EquipmentName"""
        db_obj = await service.update(
            item_id=id,
            data=data.create_instance(),
        )
        return service.to_schema(db_obj)

    @delete(
        path=urls.ITEM_NAME_DELETE,
        operation_id="DeleteEquipmentName",
        name="EquipmentNames:delete",
        summary="Delete EquipmentName",
        description="Delete a EquipmentName",
        # guards=[],
        return_dto=None,
    )
    async def delete_item_name(
        self,
        service: EquipmentNameService,
        id: Annotated[
            int,
            Parameter(
                title="EquipmentName id",
                description="The id of the EquipmentName to delete",
            ),
        ],
    ) -> None:
        """Delete a EquipmentName"""
        await service.delete(id)

    @get(
        path=urls.ITEM_NAME_LIST_WEB,
        name="equipment_names:list_web",
        include_in_schema=False,
    )
    async def get_list_web(
        self,
        request: Request,
        service: EquipmentNameService,
    ) -> Template:
        """Get list of departments for template"""
        results, total = await service.list_and_count()
        current_name_id = request.query_params.get("equipment_name")
        
        return Template(
            template_name="reference_book/select_template.html",
            context={
                "items": results,
                "total": total,
                "item_name_id": "name_id",
                "value_key": "id",
                "text_key": "name",
                "current_id": current_name_id,
            },
        )
