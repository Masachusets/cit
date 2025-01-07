from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.app.database.models import Document


class DocumentRepository(SQLAlchemyAsyncRepository[Document]):
    model_type = Document
