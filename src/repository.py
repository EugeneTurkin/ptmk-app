class Repository:
    create_index= """
        CREATE INDEX lname_idx on employees ( last_name asc );
    """

    create_table = """
        DROP TABLE IF EXISTS employees;
        DROP TYPE IF EXISTS sex;
        CREATE TYPE sex AS ENUM ('male', 'female');
        CREATE UNLOGGED TABLE employees (
            id BIGSERIAL PRIMARY KEY,
            last_name VARCHAR (50) NOT NULL,
            first_name VARCHAR (50) NOT NULL,
            patronymic VARCHAR(50) NOT NULL,
            birthday DATE NOT NULL,
            sex SEX NOT NULL
        );
    """

    drop_index="""
        DROP INDEX lname_idx;
    """

    get_age = """
        SELECT extract(year FROM age(birthday))
        FROM employees e
        WHERE e.last_name = %(last_name)s
        AND e.first_name = %(first_name)s
        AND e.patronymic = %(patronymic)s
        AND e.birthday = %(birthday)s;
    """
    
    get_all_unique = """
        SELECT last_name, first_name, patronymic, birthday, sex, extract(year FROM age(birthday))
        FROM employees
        GROUP BY last_name, first_name, patronymic, birthday, sex, extract(year FROM age(birthday))
        ORDER BY last_name, first_name, patronymic;
    """

    get_special = """
        SELECT * FROM employees e
        WHERE e.sex = 'male' AND e.last_name LIKE 'F%';
    """

    load = """
        INSERT INTO employees (
            last_name,
            first_name,
            patronymic,
            birthday,
            sex) VALUES (%s, %s, %s, %s, %s)
    """

    load_by_batch = """
        INSERT INTO employees (last_name, first_name, patronymic, birthday, sex)
        VALUES (
        %(last_name)s,
        %(first_name)s,
        %(patronymic)s,
        %(birthday)s,
        %(sex)s);
    """

    unopt_time = """
        EXPLAIN ANALYZE SELECT * FROM employees
        WHERE sex = 'male'
        AND last_name LIKE 'F%'
    """
