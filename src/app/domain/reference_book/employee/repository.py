from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.app.database.models.reference_book.employees import Employee


class EmployeeRepository(SQLAlchemyAsyncRepository[Employee]):

    model_type = Employee
    id_attribute = "slug"
