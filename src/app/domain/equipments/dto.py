from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.app.database.models import Equipment


class EquipmentCreateDTO(SQLAlchemyDTO[Equipment]):
    config = SQLAlchemyDTOConfig(
        exclude={
            "document_out_id",
        },
    )


class EquipmentUpdateDTO(SQLAlchemyDTO[Equipment]):
    config = SQLAlchemyDTOConfig(
        exclude={"it"},
        partial=True,
    )


class EquipmentReadDTO(SQLAlchemyDTO[Equipment]):
    config = SQLAlchemyDTOConfig(
        rename_fields={"model": "equipment_model"},
    )
