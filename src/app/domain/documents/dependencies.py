from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.documents.service import DocumentService


async def provide_document_service(
        db_session: AsyncSession | None = None,
) -> AsyncGenerator[DocumentService, None]:
    async with DocumentService.new(db_session) as service:
        yield service
