from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import SlugKey

from ..base import BaseStockModel

if TYPE_CHECKING:
    from ..equipments import Equipment


class DepartmentType(str, Enum):
    UPOGG = "upogg"
    OPK = "opk"
    POGZ = "pogz"
    STORAGE = "storage"


class Department(BaseStockModel, SlugKey):
    __tablename__ = "departments"

    slug: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    type: Mapped[DepartmentType] = mapped_column(
        default=DepartmentType.STORAGE,
    )

    # relationships
    equipments: Mapped[list[Equipment]] = relationship(
        "Equipment", back_populates="department"
    )
