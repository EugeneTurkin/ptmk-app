import argparse
import textwrap

from src.enums import Mode


parser = argparse.ArgumentParser(
    prog="python app.py",
    usage="python app.py {0, 1, 2, 3, 4, 5, 6} -d (только во втором режиме) фамилия имя отчество ГГГГ-ММ-ДД пол",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
        Приложение имеет шесть режимов работы:
            0: Генерация "фикстур" - параллельная генерация данных и последующая запись в файлы .csv
                                (если этих файлов ещё нет), использует все доступные ядра.
            1: Создание базы данных - создание реляции (таблицы) и необходимых типов. Если реляция уже существует - 
                                пересоздание с потерей всех данных, типов, индексов.
            2: Создание записи сотрудника - создание новой записи из данных, указанных в аргументе '-d'.
                                Пример: python app.py 2 Ivanov Ivan Ivanovich 1988-08-14
            3: Вывод данных - вывод всех строк реляции с уникальными значениями, отсортированных по ФИО в виде таблицы.
            4: Заполнение базы данных - запуск параллельной записи данных в базу из файлов "фикстур". Каждая строчка
                                файла парсится, оборачивается в объект модели, пакетно загружается в базу. 
            5: Вывод данных по критерию - вывод всех строк удовлетворяющих условиям: пол мужской,
                                фамилия начинается с 'F'.
            6: Замер скорости - вывод скорости выполнения режима '5' до и после оптимизации (создания индекса),
                                с последующим удалением индекса. Функционирует некорректно (проблема в драйвере БД).                            
    """),
)
parser.add_argument("mode", type=int, choices=Mode.values(), help="режим работы приложения")
parser.add_argument("-d", nargs=5, type=str, help="данные работника (фио, дата, пол)")    