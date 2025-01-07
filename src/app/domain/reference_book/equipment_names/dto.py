from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.app.database.models.reference_book.equipment_names import EquipmentName


class EquipmentNameReadCreateDTO(SQLAlchemyDTO[EquipmentName]):
    config = SQLAlchemyDTOConfig()


class EquipmentNameUpdateDTO(SQLAlchemyDTO[EquipmentName]):
    config = SQLAlchemyDTOConfig(
        exclude={"id"},
        partial=True,
    )
