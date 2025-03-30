from litestar import Controller, Request, get, delete, post, put
from litestar.di import Provide
from litestar.response import Template

from ..dependencies import provide_equipment_service
from ..service import EquipmentService, Equipment


# test_results = [
#     {
#         "it": "IT00001",
#         "serial_number": "б/н",
#         "name": {"id": 1, "name": "Name 1"},
#         "model": "Model 1",
#         "manufacture_date": "2022-01",
#         "arrival_date": "2022-01",
#         "document_in_id": None,
#         "document_out_id": None,
#         "status": "exploited",
#         "form_number": None,
#         "department": None,
#         "employee": {"slug": "slug", "name": "name"},
#         "location": None,
#         "notes": "",
#     },
#     {
#         "it": "IT00002",
#         "serial_number": "б/н",
#         "name": {"id": 2, "name": "Printer"},
#         "model": "Model 1",
#         "manufacture_date": "2024-01",
#         "arrival_date": "2024-02",
#         "document_in_id": None,
#         "document_out_id": None,
#         "status": "exploited",
#         "form_number": None,
#         "department": None,
#         "employee": {"slug": "slug1", "name": "Ivanov Ivan Ivanovich"},
#         "location": None,
#         "notes": "notes",
#     },
# ]


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
    async def create_item(self, service: EquipmentService, request: Request) -> Template:
        data: dict = await request.form()
        print("-" * 30)
        print(dict(data))
        print("-" * 30)
    
        # Валидация данных
        # item_data = EquipmentCreateSchema(**data)
    
        # item: Equipment = await service.create(data=data)
        service.create(**data)
        template_name = "partial/equipment/equipment_table.html"
        return Template(
            template_name=template_name,
        )
    
    @put(
        path="/{equipment_it:str}",
        operation_id="Web:UpdateEquipment",
        name="equipments:update_web",
    )
    async def update_item(self, service: EquipmentService, equipment_it: str) -> Template:
        item = await service.update(equipment_it)
        template_name = "partial/equipment/equipment_table.html"  # TODO: update path
        return Template(
            template_name=template_name,
            context={"item": item},
        )

    @delete(
        path="/{equipment_it:str}",
        operation_id="Web:DeleteEquipment",
        name="equipments:delete_web",
        status_code=200,  # TODO: remove
    )
    async def delete_equipment(self, service: EquipmentService, equipment_it: str) -> Template:
        await service.delete(equipment_it)
        template_name = "partial/equipment/equipment_table.html"  # TODO: update path
        return Template(
            template_name=template_name,
        )

    @get(
        path="/create",
        name="items:get_create_form_web",
    )
    async def get_create_form(self) -> Template:
        template_name = "equipment/form.html"
        return Template(
            template_name=template_name,
        )
    
    @get(
        path="/update/{equipment_it:str}",
        name="items:get_update_form_web",
    )
    async def get_update_form(self, service: EquipmentService, equipment_it: str) -> Template:
        equipment = await service.get(equipment_it)
        print(equipment.serial_number)
        template_name = "equipment/form.html"
        return Template(
            template_name=template_name,
            context={"equipment": equipment},
        )
    
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

    @get(
        path="/validate-it",
        name="items:validate_it",
    )
    async def validate_it(self, it: str, service: EquipmentService) -> Template:
        """Check IT number validity"""
        is_valid, error_message = await service.validate_it_number(it)
        
        if not is_valid:
            return Template(
                template_name="items/components/form/fields/validation-message.html",
                context={"message": error_message},
            )
        else:
            return Template(
                template_str="",
            )

    @get(
        path="/next-it",
        name="items:get_next_it",
    )
    async def get_next_it(self, service: EquipmentService) -> Template:
        """Generate next IT number"""
        next_it = await service.generate_next_it()
        return Template(
            template_name="items/components/form/fields/validation-message.html",
            context={"message": next_it},
        )
