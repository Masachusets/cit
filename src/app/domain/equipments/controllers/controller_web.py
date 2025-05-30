from litestar import Controller, Request, get, delete, post, put
from litestar.datastructures.multi_dicts import FormMultiDict
from litestar.di import Provide
from litestar.response import Template
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.app.database import EquipmentStatus

from ..dependencies import provide_equipment_service
# from ..dto import EquipmentCreateDTO
from ..service import EquipmentService, Equipment


class EquipmentWebController(Controller):
    include_in_schema = False
    path = "/equipments"
    dependencies = {"service": Provide(provide_equipment_service)}

    @get(
        path="",
        operation_id="Web:ListEquipments",
        name="items:get_list_web",
    )
    async def get_list(
        self,
        service: EquipmentService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> Template:
        results, total = await service.list_and_count()  # (*filters)
        template_name = "equipment/list.html"
        return Template(
            template_name=template_name,
            context={"equipments": results, "total": total},
        )

    # @get(
    #     path="/{item_it:str}",
    #     operation_id="Web:GetEquipment",
    #     name="items:get_web",
    # )
    # async def get_item(self, service: EquipmentService, item_it: str) -> Template:
    #     item = await service.get(item_it)
    #     template_name = "items/item-card-read.html"
    #     return Template(
    #         template_name=template_name,
    #         context={"item": item},
    #     )

    @post(
        path="/",
        operation_id="Web:CreateEquipment",
        name="equipments:create_web",
    )
    async def create_equipment(
        self, 
        service: EquipmentService, 
        request: Request,
    ) -> Template:
        data: FormMultiDict = await request.form()
    
        # Валидация данных
        # equipment_data: EquipmentCreateDTO = EquipmentCreateDTO(data)
    
        new_equipment: Equipment = await service.create_web(data=dict(data))
        template_name = "partials/equipment/equipment_row.html"
        return Template(
            template_name=template_name,
            context={
                "equipment": new_equipment,
            }
        )
    
    @put(
        path="/{equipment_it:str}",
        operation_id="Web:UpdateEquipment",
        name="equipments:update_web",
    )
    async def update_equipment(
        self, 
        service: EquipmentService, 
        request: Request,
        equipment_it: str,
    ) -> Template:
        data: FormMultiDict = await request.form()
        update_equipment = await service.update_web(data=dict(data), equipment_id=equipment_it)
        template_name = "partials/equipment/equipment_row.html"
        return Template(
            template_name=template_name,
            context={
                "equipment": update_equipment,
            },
        )

    @delete(
        path="/{equipment_it:str}",
        operation_id="Web:DeleteEquipment",
        name="equipments:delete_web",
        status_code=HTTP_200_OK,  # TODO: remove
    )
    async def delete_equipment(self, service: EquipmentService, equipment_it: str) -> Template:
        await service.delete(equipment_it)
        return Template(
            template_str=" ",
            status_code=HTTP_200_OK,
        )

    @get(
        path="/create",
        name="items:get_create_form_web",
    )
    async def get_create_form(self, service: EquipmentService) -> Template:
        next_it = await service.generate_next_it()
        template_name = "equipment/form.html"
        return Template(
            template_name=template_name,
            context={
                "next_it": next_it,
            }
        )
    
    @get(
        path="/update/{equipment_it:str}",
        name="items:get_update_form_web",
    )
    async def get_update_form(self, service: EquipmentService, equipment_it: str) -> Template:
        equipment = await service.get(equipment_it)
        template_name = "equipment/form.html"
        return Template(
            template_name=template_name,
            context={"equipment": equipment},
        )

    @get(
        path="/validate-it",
        name="equipments:validate_it",
    )
    async def validate_it(self, it: str, service: EquipmentService) -> Template:
        """Check IT number validity"""
        is_valid, error_message = await service.validate_it_number(it)
        
        if not is_valid:
            return Template(
                template_name="equipment/components/form/fields/validation-message.html",
                context={"message": error_message},
            )
        else:
            return Template(
                template_str=" ",
            )
    
    @get(
        path="/statuses",
        name="equipments:get_statuses",
    )
    async def get_all_statuses(self, request: Request) -> Template:
        current_status = request.query_params.get("status")
        return Template(
            template_name="partials/equipment/select_status.html",
            context={
                "statuses": list(EquipmentStatus),
                "current_status": current_status,
            }
        )
