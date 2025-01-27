from enum import Enum
from typing import Any, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseStockModel
from .custom_types import ITNumberType, YearMonthType

if TYPE_CHECKING:
    from .documents import Document
    from .reference_book import EquipmentName, Employee, Department


def create_relationship(
    back_populates: str = "equipments",
    lazy: str = "selectin",  # "joined"
    **kwargs: Any,
) -> relationship:
    return relationship(
        back_populates=back_populates,
        lazy=lazy,
        **kwargs,
    )


class EquipmentStatus(str, Enum):
    EXPLOITED = "exploited"
    INTERNET = "internet"
    SVT = "svt"
    FAULTY = "faulty"
    RESERVE = "reserve"
    WRITE_OFF = "write_off"


class Equipment(BaseStockModel):
    __tablename__ = "equipment"

    it: Mapped[str] = mapped_column(ITNumberType, primary_key=True)
    name_id: Mapped[int] = mapped_column(ForeignKey("equipment_names.id"))
    model: Mapped[str] = mapped_column(String, nullable=True)
    serial_number: Mapped[str] = mapped_column(String(50))
    manufacture_date: Mapped[str] = mapped_column(YearMonthType, nullable=True)
    arrival_date: Mapped[str] = mapped_column(YearMonthType, nullable=True)
    document_in_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), nullable=True
    )
    document_out_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), nullable=True
    )
    status: Mapped[EquipmentStatus] = mapped_column(default=EquipmentStatus.EXPLOITED)
    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.slug"), nullable=True
    )
    department_id: Mapped[str] = mapped_column(
        ForeignKey("departments.slug"), nullable=True
    )
    form_number: Mapped[str] = mapped_column(String(5), nullable=True)
    location: Mapped[str] = mapped_column(String(50), nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    # relationships
    name: Mapped[EquipmentName] = create_relationship()
    employee: Mapped[Employee] = create_relationship()
    department: Mapped[Department] = create_relationship()
    document_in: Mapped[Document] = create_relationship(
        back_populates="equipments_in",
        foreign_keys=[document_in_id],
    )
    document_out: Mapped[Document] = create_relationship(
        back_populates="equipments_out",
        foreign_keys=[document_out_id],
    )

    __table_args__ = (
        CheckConstraint(
            "(employee_id IS NULL) != (department_id IS NULL)",
            name="check_employee_or_department",
        ),
    )
