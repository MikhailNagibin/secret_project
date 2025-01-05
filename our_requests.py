import psycopg2
from hashlib import sha256
import json


def get_db_connection() -> psycopg2.extensions.connection:
    with open("config.json") as f:
        conf = json.load(f)
    DATABASE = conf["DATABASE"]
    USER = conf["USER"]
    PASSWORD = conf["PASSWORD"]
    HOST = conf["HOST"]
    PORT = conf["PORT"]
    conn = psycopg2.connect(
        dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    return conn


def generate_password(password): # получить хеш пароля
    return sha256(password.encode()).hexdigest()


def get_user_by_id(cur: psycopg2.extensions.cursor, id: int) -> list[tuple]: #получить информацию о польователе по его id
    cur.execute('select * from Users where id = %s', (id, ))
    return cur.fetchall()


def get_user_by_email(cur: psycopg2.extensions.cursor, email: str) -> list[tuple]:
    cur.execute('select * from Users where email = %s', (email, ))
    return cur.fetchall()


def get_role_by_id(cur: psycopg2.extensions.cursor, role: str) -> list[tuple]:
    cur.execute('select id from Roles where role = %s', (role, ))
    return cur.fetchall()

def get_roles(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("select * from Roles where role != 'Администратор'")
    return cur.fetchall()


def add_user(conn: psycopg2.extensions.connection, data: tuple) -> None: # внести нового пользователя в бд
    cur = conn.cursor()
    cur.execute(
        "insert into users(firstname, surname, email, user_password, role_id) values (%s, %s, %s, %s, %s)",
        data,
    )
    conn.commit()
