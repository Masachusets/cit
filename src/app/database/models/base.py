from sqlalchemy.orm import DeclarativeBase
from advanced_alchemy.base import CommonTableAttributes, orm_registry


class BaseStockModel(CommonTableAttributes, DeclarativeBase):
    __abstract__ = True

    registry = orm_registry
