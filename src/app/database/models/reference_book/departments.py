from enum import Enum
from sqlalchemy import String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import BaseStockModel


class DepartmentType(str, Enum):
    UPOGG = "upogg"
    OPK = "opk"
    POGZ = "pogz"
    STORAGE = "storage"


class Department(BaseStockModel):
    __tablename__ = "departments"

    slug: Mapped[str] = mapped_column(String(20), primary_key=True, default="storage")
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[DepartmentType] = mapped_column(
        SQLAlchemyEnum(DepartmentType),
        nullable=False,
        default=DepartmentType.STORAGE,
    )

    # relationships
    equipments: Mapped[list["Equipment"]] = relationship(
        "Equipment", back_populates="department"
    )
