import re
from typing import NewType

from sqlalchemy import TypeDecorator, String
from sqlalchemy.exc import ArgumentError


class FixedChar7(TypeDecorator):
    """
    Custom SQLAlchemy type for a string of exactly 7 characters.
    """
    impl = String(7)  # Underlying database type

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        """
        Called when loading data from the database.
        No transformation needed here since the database already enforces the length.
        """
        return value

    def copy(self, **kw):
        """
        Required for SQLAlchemy to properly handle the type.
        """
        return FixedChar7(self.impl.length)


class YearMonthType(FixedChar7):
    """
    Custom SQLAlchemy type for a string in the format 'YYYY-MM'.
    """

    def process_bind_param(self, value, dialect):
        """
        Validate and ensure the value is in 'YYYY-MM' format.
        """
        if value is not None:

            # Validate the format using a regex
            if not re.match(r"^\d{4}-\d{2}$", value):
                raise ArgumentError(f"Value must be in 'YYYY-MM' format, got '{value}'.")

            # Validate the month is between 01 and 12
            year, month = map(int, value.split('-'))
            if not (1 <= month <= 12):
                raise ArgumentError(f"Month must be between 01 and 12, got '{month}'.")

            # Validate the year is between 1980 and 3000
            if not (1980 <= year <= 3000):
                raise ArgumentError(f"Year must be between 1980 and 3000, got '{year}'.")

        return value


class ITNumberType(FixedChar7):
    """
    Custom SQLAlchemy type for a string in the format 'IT12345'.
    """

    def process_bind_param(self, value, dialect):
        """
        Validate and ensure the value is in 'IT12345' format.
        """
        # Validate the format using a regex
        if value is not None:
            if not re.match(r"^it\d{5}$", value):
                raise ArgumentError(f"Value must be in 'IT12345' format, got '{value}'.")

        return value
