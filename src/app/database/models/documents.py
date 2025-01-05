from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import BigIntPrimaryKey
from .base import BaseStockModel
from datetime import date


class Document(BaseStockModel):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigIntPrimaryKey)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    doc_number: Mapped[str] = mapped_column(String(10), nullable=False)
    doc_date: Mapped[date] = mapped_column(Date, nullable=True, default=date.today)
    comment: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # relationships

    incoming_equipments: Mapped[list["Equipment"]] = relationship(
        "Equipment",
        foreign_keys="[Equipment.incoming_document_id]",
        back_populates="incoming_document",
    )
    outgoing_equipments: Mapped[list["Equipment"]] = relationship(
        "Equipment",
        foreign_keys="[Equipment.outgoing_document_id]",
        back_populates="outgoing_document",
    )
