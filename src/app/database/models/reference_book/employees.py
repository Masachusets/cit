from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import SlugKey

from ..base import BaseStockModel

if TYPE_CHECKING:
    from ..equipments import Equipment


class Employee(BaseStockModel, SlugKey):
    __tablename__ = "employees"

    slug: Mapped[str] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), unique=True)
    card_number: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # relationships

    equipments: Mapped[list[Equipment]] = relationship(
        "Equipment", back_populates="employee"
    )
