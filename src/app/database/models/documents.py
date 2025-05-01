from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import BigIntPrimaryKey
from .base import BaseStockModel
from datetime import date

if TYPE_CHECKING:
    from .equipments import Equipment


class Document(BaseStockModel, BigIntPrimaryKey):
    __tablename__ = "documents"

    type: Mapped[str] = mapped_column(String(50), nullable=False)
    doc_number: Mapped[str] = mapped_column(String(10), nullable=False)
    doc_date: Mapped[date | None] = mapped_column(Date, nullable=True, default=date.today)
    comment: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # relationships

    equipments_in: Mapped[list[Equipment]] = relationship(
        "Equipment",
        foreign_keys="[Equipment.document_in_id]",
        back_populates="document_in",
    )
    equipments_out: Mapped[list[Equipment]] = relationship(
        "Equipment",
        foreign_keys="[Equipment.document_out_id]",
        back_populates="document_out",
    )
