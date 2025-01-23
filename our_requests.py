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


def generate_password(password: str) -> str:  # получить хеш пароля
    return sha256(password.encode()).hexdigest()


def get_user_by_id(cur: psycopg2.extensions.cursor, id: int) -> list[tuple]:  # получить информацию о польователе по его id
    cur.execute("select * from Users where id = %s", (id,))
    return cur.fetchall()


def get_user_by_email(cur: psycopg2.extensions.cursor, email: str) -> list[tuple]:
    cur.execute("select * from Users where email = %s", (email,))
    return cur.fetchall()


def get_inventory_name_id_by_name(cur: psycopg2.extensions.cursor, name: str) -> list[tuple]:
    cur.execute('select id from  inventory_name '
                'where name = %s', (name, ))
    return cur.fetchall()


def add_inventory_name_and_get_it_id(conn: psycopg2.extensions.connection, name: str) -> None:
    cur = conn.cursor()
    cur.execute("insert into inventory_name(name) values (%s)", (name, ))
    conn.commit()


def get_all_from_inventory_name(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('Select * from inventory_name')
    return cur.fetchall()


def get_role_by_id(cur: psycopg2.extensions.cursor, id: str) -> list[tuple]:
    cur.execute("select role from Roles where id = %s", (id,))
    return cur.fetchall()


def get_roles(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("select * from Roles where role != 'Администратор'")
    return cur.fetchall()


def add_user(conn: psycopg2.extensions.connection, data: tuple ) -> None:  # внести нового пользователя в бд
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


def get_conditions(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("select * from conditions")
    return cur.fetchall()


def get_free_inventory_for_zacrep(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("select i.name, i_n.name from inventory as i inner join inventory_name as i_n on i.name = i_n.id group by i_n.name, i.name order by i_n.name")
    return cur.fetchall()


def get_free_inventory_for_read(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute(
        """select i_n.name, count(*), c.condition from inventory as i inner join conditions as c on i.condition_id = c.id
                    inner join inventory_name as i_n on i_n.id = i.name
                   where i.user_id = -1
                   group by i_n.name, c.condition, i.condition_id
                   order by i.condition_id, i_n.name"""
    )
    return cur.fetchall()


def get_condition_id_by_condition(
    cur: psycopg2.extensions.cursor, condition: str) -> list[tuple]:
    cur.execute("select id from conditions where condition = %s", (condition,))
    return cur.fetchall()


def delete_inventory_by_name_and_condition_id(
    conn: psycopg2.extensions.connection, name: int, condition_id:int) -> None:
    cur = conn.cursor()
    cur.execute(
        "Delete from inventory "
        "where name = %s and condition_id = %s",
        (name, condition_id),
    )
    conn.commit()


def create_plane(conn: psycopg2.extensions.connection, data: tuple) -> None:
    cur = conn.cursor()
    cur.execute("""insert into purchase_plan(name, count, price, supplier) 
                values(%s, %s, %s, %s)""", data)
    conn.commit()


def create_report(conn: psycopg2.extensions.connection, name: str, report: str) -> None:
    cur = conn.cursor()
    cur.execute("""insert into reports(name, report) values(%s, %s)""", (name, report))
    conn.commit()


def get_occupied_inventory(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("""select u.firstname, u.surname, i_n.name, count(*) from users as u inner join inventory as i on i.user_id = u.id
                   inner join inventory_name as i_n  on i.name = i_n.id
                   where u.id > 0
                   group by u.firstname, i_n.name, u.surname
                   order by u.firstname , u.surname;""")
    return cur.fetchall()


def get_users_id_firstname_and_surname(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('select id, firstname, surname from users where role_id > 1 order by firstname, surname')
    return cur.fetchall()


def get_count_of_free_inventory_by_name(cur: psycopg2.extensions.cursor, name: int) -> list[tuple]:
    cur.execute('select count(*) from inventory where name = %s and user_id = -1 group by name', (name, ))
    return cur.fetchall()


def securing_inventory(conn: psycopg2.extensions.connection, user_id: int, name: int, quantity: int) -> None:
    cur = conn.cursor()
    cur.execute("""update inventory 
                    set user_id = %s where id in (select id from inventory 
                    where name = %s and user_id = -1 
                    order by condition_id 
                    limit %s)""", (user_id, name, quantity))
    conn.commit()


def get_status_id_by_status(cur: psycopg2.extensions.cursor, status: str) -> list[tuple]:
    cur.execute('select id from request_status where status = %s', (status, ))
    return cur.fetchall()


def add_request(conn: psycopg2.extensions.connection, user_id: int, inventory_id, count: int, status_id: int) -> None:
    cur = conn.cursor()
    cur.execute("insert into requests(user_id, inventory_name_id, count, status_id) values(%s, %s, %s, %s)",
                (user_id, inventory_id, count, status_id))
    conn.commit()


def get_my_requests(cur: psycopg2.extensions.cursor, user_id: int) -> list[tuple]:
    cur.execute("""select r.id, i_n.name, r.count, rs.status from inventory_name as i_n inner join requests as r on r.inventory_name_id = i_n.id 
	                     inner join request_status as rs on r.status_id = rs.id
                         where r.user_id = %s order by r.id""", (user_id,))
    return cur.fetchall()


def get_user_id_by_fullname(cur: psycopg2.extensions.cursor, name: str, surname: str) -> list[tuple]:
    cur.execute('select id from users '
                'where firstname = %s and surname = %s', (name, surname))
    return cur.fetchall()


def detaching_inventory(conn: psycopg2.extensions.connection, user_id: int, name: int) -> None:
    cur = conn.cursor()
    cur.execute("""update inventory 
                         set user_id = -1 
                         where name = %s and user_id = %s""", (name, user_id))
    conn.commit()


def get_requests(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("""select r.id, u.firstname, u.surname, i_n.name, r.count from users as u inner join requests as r on r.user_id = u.id
                   inner join inventory_name as i_n on i_n.id = r.inventory_name_id
                   where r.status_id in (select id from request_status where status = 'Не рассмотрен')""")
    return cur.fetchall()


def change_status_id(conn: psycopg2.extensions.connection, request_id: int, status_id: int) -> None:
    cur = conn.cursor()
    cur.execute('update requests set status_id = %s where id = %s', (status_id, request_id))
    conn.commit()


def delete_request(conn: psycopg2.extensions.connection, request_id: int):
    cur = conn.cursor()
    cur.execute('delete from requests where id = %s', (request_id, ))
    conn.commit()


def add_repair_requests(conn: psycopg2.extensions.connection, data: tuple) -> None:
    cur = conn.cursor()
    cur.execute("insert into repair_requests(inventory_name_id, count, replace) values (%s,%s, %s)", data)
    conn.commit()


def get_inventory_by_user_id(cur: psycopg2.extensions.cursor, user_id):
    cur.execute("""select u.firstname, u.surname, i_n.name, count(*) from users as u inner join inventory as i on i.user_id = u.id
                         inner join inventory_name as i_n  on i.name  = i_n.id
                       where u.id = %s
                       group by u.firstname, i_n.name, u.surname
                       order by u.firstname , u.surname;""", (user_id, ))
    return cur.fetchall()


def get_all_purchases(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("select * from purchase_plan")
    return cur.fetchall()


def delete_purchase(conn: psycopg2.extensions.connection, num: int)  -> None:
    cur  = conn.cursor()
    cur.execute('delete from purchase_plan  where id = %s', (num, ))
    conn.commit()


def get_all_reports(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute('select r.id, u.firstname, u.surname,  r.report  from reports as r inner join users as u on u.id = r.name')
    return cur.fetchall()


def delete_report_by_id(conn: psycopg2.extensions.connection, num: int) -> None:
    cur = conn.cursor()
    cur.execute('delete from reports where id = %s', (num, ))
    conn.commit()