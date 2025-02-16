from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.app.database.models.reference_book.departments import Department


class DepartmentReadCreateDTO(SQLAlchemyDTO[Department]):
    config = SQLAlchemyDTOConfig(
        exclude={"equipments"},
    )


class DepartmentUpdateDTO(SQLAlchemyDTO[Department]):
    config = SQLAlchemyDTOConfig(
        exclude={"slug"},
        partial=True,
    )
