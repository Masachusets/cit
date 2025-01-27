from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.app.database.models import Equipment


class EquipmentRepository(SQLAlchemyAsyncRepository[Equipment]):
    model_type = Equipment
    id_attribute = "it"
