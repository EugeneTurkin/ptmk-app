from multiprocessing import Pool, cpu_count
from pathlib import Path
from random import choice, randint
import string
from typing import Generator, Any

import psycopg2

from src.enums import Sex
from src.models import Employee
from src.validators import data_validated


def generate_employee() -> dict[str, Any]:
    chars = string.ascii_lowercase
    no_f_chars = chars.replace("f", "")
    months = [str(0) + str(i) if i < 10 else str(i) for i in range(1, 13)]
    days = [str(0) + str(i) for i in range(1, 10)] + [str(i) for i in range(10, 29)]

    gen_name = lambda a, b: "".join([choice(chars) for _ in range(randint(a, b))]).title()
    gen_last_name = lambda a, b: "".join([choice(no_f_chars)] + [choice(chars) for _ in range(randint(a, b))]).title()
    gen_bday = str(randint(1930, 2006)) + "-" + choice(months) + "-" + choice(days)
    gen_sex = choice(Sex.values())
    employee = Employee(
        last_name=gen_last_name(3, 49),
        first_name=gen_name(3, 50),
        patronymic=gen_name(3, 50),
        birthday=gen_bday,
        sex=gen_sex,
    )
    return employee.attributes


def generate_employee_special() -> dict[str, Any]:
    chars = string.ascii_lowercase
    months = [str(0) + str(i) if i < 10 else str(i) for i in range(1, 13)]
    days = [str(0) + str(i) for i in range(1, 10)] + [str(i) for i in range(10, 29)]
    
    gen_name = lambda a, b: "".join([choice(chars) for _ in range(randint(a, b))]).title()
    gen_last_name = lambda a, b: "".join(["F"] + [choice(chars) for _ in range(randint(a, b))]).title()
    gen_bday = str(randint(1930, 2006)) + "-" + choice(months) + "-" + choice(days)
    employee = Employee(
        last_name=gen_last_name(3, 49),
        first_name=gen_name(3, 50),
        patronymic=gen_name(3, 50),
        birthday=gen_bday,
        sex=Sex.MALE.value,
    )
    return employee.attributes


def generative_worker(cpu_id: int) -> Path:
    file_path = Path.cwd() / "fixtures" / "fixtures{}.csv".format(cpu_id)

    try:
        f = open(file_path, "+a")
        for _ in range(1_000_000 // cpu_count()):
            e = generate_employee()
            f.write(";".join([e["last_name"], e["first_name"], e["patronymic"], e["birthday"], e["sex"]]) + "\n")
        return file_path
    finally:
        f.close()


def uploading_worker(file_path: Path) -> None:
    file_path = Path.cwd() / "fixtures" / file_path
    conn = psycopg2.connect(
        database="postgres",
        user="pu",
        password="pp",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()
    try:
        Employee.load_by_batch(cur, file_iterator(file_path))
    finally:
        conn.commit()
        cur.close()
        conn.close()


def file_iterator(file_path: Path) -> Generator[dict[str, Any], Any, Any]:
    with open(file_path) as f:
        for line in f:
            data = line.rstrip("\n").split(";")
            if data_validated(data):
                yield Employee.create_object(data).attributes
            else:
                raise ValueError("Trying to upload corrupted data from .csv file")


def generate_fixtures() -> None:
    with Pool(cpu_count()) as pool:
        paths = pool.map(generative_worker, [i for i in range(cpu_count())])
    with open(paths[0], "a") as f:
        for _ in range(100):
            e = generate_employee_special()
            f.write(";".join([e["last_name"], e["first_name"], e["patronymic"], e["birthday"], e["sex"]]) + "\n")


def upload_fixtures(fixtures) -> None:
    with Pool(cpu_count()) as pool:
        pool.map(uploading_worker, fixtures)
