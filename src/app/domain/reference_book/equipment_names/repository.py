from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.app.database.models.reference_book.equipment_names import EquipmentName


class EquipmentNameRepository(SQLAlchemyAsyncRepository[EquipmentName]):

    model_type = EquipmentName
