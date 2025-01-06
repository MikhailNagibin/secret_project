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


def generate_password(password: str) -> str: # получить хеш пароля
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
        "insert into users(firstname, surname, email, user_password, role_id) "
        "values (%s, %s, %s, %s, %s)",
        data,
    )
    conn.commit()


def add_inventory(conn: psycopg2.extensions.connection, data: tuple) -> None:
    cur = conn.cursor()
    cur.execute("insert into inventory(name, condition_id) values (%s, %s)", data)
    conn.commit()


def get_all_inventory_without_condition(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('select name, count(*) from inventory group by name')
    return cur.fetchall()


def get_conditions(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('select * from conditions')
    return cur.fetchall()

def get_free_inventory(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('select name, count(*) from invetory where user_id = -1 group by name')
    return cur.execute()


def get_free_inventory_for_read(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("""select i.name, count(*), c.condition from inventory as i inner join conditions as c on i.condition_id = c.id
                   where i.user_id = -1
                   group by i.name, c.condition, i.condition_id
                   order by i.condition_id, i.name""")
    return cur.fetchall()

def get_conditions(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('select * from conditions')
    return cur.fetchall()