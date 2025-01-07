from advanced_alchemy.base import AdvancedDeclarativeBase, CommonTableAttributes, orm_registry


class BaseStockModel(CommonTableAttributes, AdvancedDeclarativeBase):
    __abstract__ = True

    registry = orm_registry
