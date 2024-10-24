import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="pu",
    password="pp",
    host="localhost",
    port="5432",
)
