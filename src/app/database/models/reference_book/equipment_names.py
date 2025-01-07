from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import BigIntPrimaryKey

from ..base import BaseStockModel


class EquipmentName(BaseStockModel, BigIntPrimaryKey):
    __tablename__ = "equipment_names"

    name: Mapped[str] = mapped_column(String(100))
    nomenclature_code: Mapped[str] = mapped_column(String(15), unique=True)

    # relationships

    equipments: Mapped[list["Equipment"]] = relationship(
        "Equipment", back_populates="name"
    )
