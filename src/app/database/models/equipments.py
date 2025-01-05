from enum import Enum
from sqlalchemy import String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseStockModel
from datetime import date


class EquipmentStatus(str, Enum):
    EXPLOITED = "exploited"
    INTERNET = "internet"
    SVT = "svt"
    FAULTY = "faulty"
    RESERVE = "reserve"
    WRITE_OFF = "write_off"


class Equipment(BaseStockModel):
    __tablename__ = "equipment"

    inventory_number: Mapped[str] = mapped_column(String(7), primary_key=True)
    name_id: Mapped[int] = mapped_column(ForeignKey("equipment_names.id"))
    model: Mapped[str] = mapped_column(String, nullable=True)
    serial_number: Mapped[str] = mapped_column(String(50))
    manufacture_date: Mapped[date] = mapped_column(Date, nullable=True)
    arrival_date: Mapped[date] = mapped_column(Date, nullable=True)
    incoming_document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), nullable=True
    )
    outgoing_document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), nullable=True
    )
    status: Mapped[EquipmentStatus] = mapped_column(
        EquipmentStatus, default=EquipmentStatus.EXPLOITED
    )
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
    name: Mapped["EquipmentName"] = relationship(
        "EquipmentName", back_populates="equipments"
    )
    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="equipments"
    )
    department: Mapped["Department"] = relationship(
        "Department", back_populates="equipments"
    )
    incoming_document: Mapped["Document"] = relationship(
        "Document", foreign_keys=[incoming_document_id]
    )
    outgoing_document: Mapped["Document"] = relationship(
        "Document", foreign_keys=[outgoing_document_id]
    )

    __table_args__ = (
        CheckConstraint(
            "(employee_id IS NULL) != (department_id IS NULL)",
            name="check_employee_or_department",
        ),
    )
