from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from litestar import Controller, get, post, delete, patch
from litestar.di import Provide
from litestar.response import Template

from src.app.domain.documents import urls
from src.app.domain.documents.dependencies import provide_document_service
from src.app.domain.documents.dto import (
    DocumentReadDTO,
    DocumentCreateDTO,
    DocumentUpdateDTO,
)
from src.app.domain.documents.service import DocumentService
from src.app.database.models import Document

if TYPE_CHECKING:
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Parameter


class DocumentController(Controller):

    dependencies = {"service": Provide(provide_document_service)}
    tags = ["Document"]
    return_dto = DocumentReadDTO

    @get(
        path=urls.DOCUMENT_LIST,
        operation_id="ListDocuments",
        name="documents:list",
        summary="Get list of documents",
        description="Get list of documents",
    )
    async def get_list(
            self,
            service: DocumentService,
            # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Document]:
        results, total = await service.list_and_count()  # (*filters)
        return service.to_schema(
            data=results,
            total=total,
            # filters=filters,
        )

    @get(
        path=urls.DOCUMENT_DETAIL,
        operation_id="GetDocument",
        name="documents:get",
        summary="Get document",
        description="Retrieve the details of a document",
    )
    async def get_document(
            self,
            service: DocumentService,
            document_id: Annotated[
                int,
                Parameter(
                    title="Document ID",
                    description="The ID of the document to retrieve",
                ),
            ],
    ) -> Document:
        """"""
        db_obj = await service.get(document_id)
        return service.to_schema(db_obj)

    @post(
        path=urls.DOCUMENT_CREATE,
        operation_id="CreateDocument",
        name="documents:create",
        summary="Create document",
        description="Create a new document",
        # guards=[],
        cache_control=None,
        dto=DocumentCreateDTO,
    )
    async def create_document(
            self,
            service: DocumentService,
            data: DTOData[Document],
    ) -> Document:
        """Create a new document"""
        db_obj = await service.create(data.create_instance())
        return service.to_schema(db_obj)

    @patch(
        path=urls.DOCUMENT_UPDATE,
        operation_id="UpdateDocument",
        name="documents:update",
        summary="Update a document",
        description="Update the details of a document",
        # guards=[],
        dto=DocumentUpdateDTO,
    )
    async def update_document(
            self,
            service: DocumentService,
            data: DTOData[Document],
            document_id: Annotated[
                int,
                Parameter(
                    title="Document ID",
                    description="The ID of the document to update",
                ),
            ]
    ) -> Document:
        """Update a document"""
        db_obj = await service.update(
            item_id=document_id,
            data=data.create_instance(),
        )
        return service.to_schema(db_obj)

    @delete(
        path=urls.DOCUMENT_DELETE,
        operation_id="DeleteDocument",
        name="documents:delete",
        summary="Delete document",
        description="Delete a document",
        # guards=[],
        return_dto=None,
    )
    async def delete_document(
            self,
            service: DocumentService,
            document_id: Annotated[
                int,
                Parameter(
                    title="Document ID",
                    description="The ID of the document to delete",
                ),
            ],
    ) -> None:
        """Delete a document"""
        await service.delete(document_id)

    @get(
        path=urls.DOCUMENT_LIST_WEB,
        operation_id="Web:ListDocuments",
        name="documents:list_web",
        summary="Get list of documents",
        description="Get list of documents for template",
        include_in_schema=False,
    )
    async def get_list_web(
            self,
            service: DocumentService,
            # filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> Template:
        """Get list of departments for template"""
        docs, total = await service.list_and_count()  # (*filters)
        template_name = "reference_book/documents.html"
        return Template(
            template_name=template_name,
            context={"docs": docs, "total": total},
        )
