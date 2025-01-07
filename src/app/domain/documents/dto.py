from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.app.database.models import Document


class DocumentCreateDTO(SQLAlchemyDTO[Document]):
    config = SQLAlchemyDTOConfig(
        exclude={"id"},
    )


class DocumentUpdateDTO(SQLAlchemyDTO[Document]):
    config = SQLAlchemyDTOConfig(
        exclude={"id"},
        partial=True,
    )


class DocumentReadDTO(SQLAlchemyDTO[Document]):
    config = SQLAlchemyDTOConfig()
