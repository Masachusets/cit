from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.app.domain.documents.repository import DocumentRepository, Document

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class DocumentService(SQLAlchemyAsyncRepositoryService[Document]):
    repository_type: SQLAlchemyAsyncRepository = DocumentRepository  # type: ignore
    match_fields = ["type", "number", "doc_date", "comment"]
