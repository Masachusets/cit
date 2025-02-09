from litestar import Controller, get
from litestar.di import Provide
from litestar.response import Template


from ..dependencies import provide_equipment_service
from ..service import EquipmentService


class EquipmentWebController(Controller):
    include_in_schema = False
    path = "/items"
    dependencies = {"service": Provide(provide_equipment_service)}

    @get(
        path="",
        operation_id="Web:ListEquipments",
        name="items:list_web",
    )
    async def get_list(
        self,
        service: EquipmentService,
        # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> Template:
        results, total = await service.list_and_count()  # (*filters)
        template_name = "items/items-list.html"
        return Template(
            template_name=template_name,
            context={"items": results, "total": total},
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

    # @post(
    #     path="/",
    #     operation_id="Web:CreateEquipment",
    #     name="items:create_web",
    # )
    # async def create_item(self, service: EquipmentService, request: Request) -> Template:
    #     data: dict = await request.form()
    #     print("-" * 30)
    #     print(dict(data))
    #     print("-" * 30)
    #
    #     # Валидация данных
    #     item_data = EquipmentCreateSchema(**data)
    #
    #     # item: Equipment = await service.create(data=data)
    #     template_name = "items/item-card-read.html"
    #     return Template(
    #         template_name=template_name,
    #         context={"item": data},
    #     )
    #
    # @put(
    #     path="/{item_it:str}",
    #     operation_id="Web:UpdateEquipment",
    #     name="items:update_web",
    # )
    # async def update_item(self, service: EquipmentService, item_it: str) -> Template:
    #     item = await service.update(item_it)
    #     template_name = "items/item-card-read.html"  # TODO: update path
    #     return Template(
    #         template_name=template_name,
    #         context={"item": item},
    #     )

    # @delete(
    #     path="/{item_it:str}",
    #     operation_id="Web:DeleteEquipment",
    #     name="items:delete_web",
    # )
    # async def delete_item(self, service: EquipmentService, item_it: str) -> Template:
    #     item = await service.delete(item_it)
    #     template_name = "items/item-card-read.html"  # TODO: update path
    #     return Template(
    #         template_name=template_name,
    #         context={"item": item},
    #     )

    # @get(
    #     path="/form",
    #     name="items:get_form_web",
    # )
    # async def get_form(self, item: Equipment | None = None) -> Template:
    #     if item:
    #         template_name = "items/item-card-update.html"
    #     else:
    #         template_name = "items/item-card-create.html"
    #     return Template(
    #         template_name=template_name,
    #         context={"item": item, "item_statuses": Status},
    #     )
    #
    # @get(
    #     path="/toogle-binding",
    #     name="items:toggle_binding",
    # )
    # async def edit_item(self, binding_type: str) -> Template:
    #     """
    #
    #     :param binding_type: str - type of binding
    #     :return: Template - employee or department
    #     """
    #     if binding_type == "employee":
    #         template_name = "items/components/form/fields/employee.html"
    #     else:
    #         template_name = "items/components/form/fields/department.html"
    #     return Template(
    #         template_name=template_name,
    #     )
