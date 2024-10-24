from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from prettytable import PrettyTable

from src.args import parser
from src.database import conn
from src.models import Employee
from src.populate import generate_fixtures, upload_fixtures
from src.validators import data_validated


if TYPE_CHECKING:
    from argparse import ArgumentParser
    from psycopg2._psycopg import connection, cursor


def main(conn: connection, cur: cursor, parser: ArgumentParser):
    args = parser.parse_args()
    mode = args.mode
    data = args.d
    fixture_files = [fpath for fpath in (Path.cwd() / "fixtures").glob("fixtures*.csv")]

    if mode != 2 and data is not None:
        parser.exit(message="Только режим работы '2' принимает дополнительные аргументы")
    if mode == 2 and data_validated(data) is False:
        parser.exit(
            message="Ошибка в аргументах\nПример использования: python app.py 2 Ivanov Ivan Ivanovich 1988-08-14",
        )

    if mode == 0:
        if not fixture_files:
            generate_fixtures()
        else:
            print("Похоже что фикстуры уже сгенерированы.")

    if mode == 1:
        Employee.create_table(cur)

    if mode == 2:
        new_employee = Employee.create_object(data)
        new_employee.load(cur)
        msg = "Создан и загружен сотрудник {} {} {}, возраст - {} полных лет.".format(
            new_employee.last_name,
            new_employee.first_name,
            new_employee.patronymic,
            new_employee.get_age(cur),
        )
        print(msg)

    if mode == 3:
        table = PrettyTable()
        table.field_names = ["last name", "first name", "patronymic", "birthday", "sex", "age"]
        table.add_rows(Employee.get_all_unique(cur))
        print(table)
    
    if mode == 4:
        upload_fixtures(fixture_files)
    
    if mode == 5:
        table = PrettyTable()
        table.field_names = ["last name", "first name", "patronymic", "birthday", "sex", "age"]
        table.add_rows(Employee.get_special(cur))
        print(table)
        print("Время выполнения: {}".format(Employee.unoptimized_time(cur)))

    if mode == 6:
        time = Employee.unoptimized_time
        print(time(cur))
        with Employee.optimized_state(conn, cur):
            print(time(cur))
        print(time(cur))


if __name__ == "__main__":
    with conn as connect:
        with connect.cursor() as cur:
            main(connect, cur, parser)
