from datetime import datetime
from typing import Any

import msgspec

from src.app.database.models.equipments import EquipmentStatus


class BaseStruct(msgspec.Struct):
    def to_dict(self) -> dict[str, Any]:
        return {
            f: getattr(self, f)
            for f in self.__struct_fields__
            if getattr(self, f, None) != msgspec.UNSET
        }


class EquipmentCreateSchema(BaseStruct, kw_only=True):
    it: str
    serial_number: str = "б/н"
    item_name_id: int | None
    item_model: str | None
    date_of_manufacture: str
    date_of_arrival: datetime.date = datetime.today()
    document_in_id: int | None
    document_out_id: int | None
    status: EquipmentStatus = EquipmentStatus.EXPLOITED
    number_of_form: str | None
    employee_slug: str | None
    department_slug: str | None
    number_of_consignment: str | None
    location: str | None
    comment: str

    def __post_init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_it()
        self.validate_date_of_manufacture()

    def validate_it(self):
        if not (
            self.it.startswith("ИТ") and self.it[2:].isdigit() and len(self.it) == 7
        ):
            raise ValueError(
                'Значение it должно быть строкой из 7 символов, первые два из которых "ИТ", а затем пять цифр.'
            )

    def validate_date_of_manufacture(self):
        if not self.date_of_manufacture or self.date_of_manufacture.count("-") != 1:
            raise ValueError("Значение date_of_prod должно быть в формате YYYY-MM.")
        year, month = self.date_of_manufacture.split("-")
        if not (
            year.isdigit()
            and month.isdigit()
            and 1980 <= int(year) <= 2050
            and 1 <= int(month) <= 12
        ):
            raise ValueError(
                "Значение date_of_prod должно быть в формате YYYY-MM и соответствовать диапазону годов и месяцев."
            )
