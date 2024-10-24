from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any, ClassVar, TYPE_CHECKING, Generator, Iterable

import psycopg2.extras

from src.enums import Sex
from src.repository import Repository


if TYPE_CHECKING:
    from psycopg2._psycopg import connection, cursor


@dataclass
class Employee:
    last_name: str
    first_name: str
    patronymic: str
    birthday: datetime
    sex: Sex
    _sql_repo: ClassVar[Repository] = Repository

    @property
    def attributes(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "patronymic": self.patronymic,
            "birthday": self.birthday,
            "sex": self.sex,
        }

    def load(self, cursor: cursor) -> None:
        cursor.execute(
            self._sql_repo.load,
            (
                self.last_name,
                self.first_name,
                self.patronymic,
                self.birthday,
                self.sex,
            )
        )

    def get_age(self, cursor: cursor) -> Decimal:
        cursor.execute(
            self._sql_repo.get_age,
            self.attributes
        )
        return cursor.fetchone()[0]
    
    @classmethod
    def unoptimized_time(cls, cursor: cursor) -> str:
        cursor.execute(cls._sql_repo.unopt_time)
        return cursor.fetchall()[-1][0].split(": ")[-1]
    
    @classmethod
    @contextmanager
    def optimized_state(cls, connection: connection, cursor: cursor) -> Generator[Any, Any, Any]:
        try:
            cursor.execute(cls._sql_repo.create_index)
            connection.commit()

            yield

            cursor.execute(cls._sql_repo.drop_index)
            connection.commit()
        
        finally:
            pass

    @classmethod
    def create_object(cls, data: list[str]) -> Employee:
        new_object = Employee(
            last_name=data[0].title(),
            first_name=data[1].title(),
            patronymic=data[2].title(),
            birthday=date.fromisoformat(data[3]),
            sex=Sex(data[4]).value,
        )
        return new_object
    
    @classmethod
    def load_by_batch(cls, cursor: cursor, iterable: Iterable):
        psycopg2.extras.execute_batch(
            cursor,
            cls._sql_repo.load_by_batch,
            iterable,
            10000
        )

    @classmethod
    def get_special(cls, cursor: cursor) -> list[tuple[Any]]:
        cursor.execute(cls._sql_repo.get_special)
        return cursor.fetchall()

    @classmethod
    def get_all_unique(cls, cursor: cursor) -> list[tuple[Any]]:
        cursor.execute(cls._sql_repo.get_all_unique)
        return cursor.fetchall()

    @classmethod
    def create_table(cls, cursor: cursor) -> None:
        cursor.execute(cls._sql_repo.create_table)
