from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.app.database.models import Equipment


class EquipmentCreateDTO(SQLAlchemyDTO[Equipment]):
    config = SQLAlchemyDTOConfig(
        exclude={"name", "employee", "department", "document_in", "document_out"},
    )


class EquipmentUpdateDTO(SQLAlchemyDTO[Equipment]):
    config = SQLAlchemyDTOConfig(
        exclude={"it", "name", "employee", "department", "document_in", "document_out"},
        partial=True,
    )


class EquipmentReadDTO(SQLAlchemyDTO[Equipment]):
    config = SQLAlchemyDTOConfig()
