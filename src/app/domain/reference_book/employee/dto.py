from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.app.database.models.reference_book.employees import Employee


class EmployeeCreateDTO(SQLAlchemyDTO[Employee]):
    config = SQLAlchemyDTOConfig(
        # exclude={"id"},
    )


class EmployeeUpdateDTO(SQLAlchemyDTO[Employee]):
    config = SQLAlchemyDTOConfig(
        exclude={"slug", "fullname"},
        partial=True,
    )


class EmployeeReadDTO(SQLAlchemyDTO[Employee]):
    config = SQLAlchemyDTOConfig()
