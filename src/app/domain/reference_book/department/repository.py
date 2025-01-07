from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.app.database.models.reference_book.departments import Department


class DepartmentRepository(SQLAlchemyAsyncRepository[Department]):

    model_type = Department
    id_attribute = "slug"
