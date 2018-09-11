import sqlite3
from pathlib import Path
from abc import ABC, abstractmethod

from classes import User, Publication, Payment, Order


class Database:

    DB_NAME = "database.sqlite3"
    DB_FOLDER = Path.cwd()
    DB_PATH = DB_FOLDER/DB_NAME

    DB_INSTANCE = None

    INIT_SCRIPT = Path.cwd()/"database"/"init_script.sql"

    @classmethod
    def init(cls, db_path=None):
        if db_path is not None:
            cls.DB_PATH = db_path

        # If using in-memory DB or DB file does not exist - create DB
        if cls.DB_PATH == ":memory:" or not cls.DB_PATH.exists():
            cls.DB_INSTANCE = sqlite3.connect(cls.DB_PATH)
            with cls.DB_INSTANCE as conn:
                with open(cls.INIT_SCRIPT, 'rt') as sql_file:
                    conn.executescript(sql_file.read())
        else:
            cls.DB_INSTANCE = sqlite3.connect(cls.DB_PATH)

        cls.DB_INSTANCE.row_factory = sqlite3.Row

    @classmethod
    def is_initialised(cls):
        return bool(cls.DB_INSTANCE)

    @classmethod
    def load_all(cls):
        conn = cls.DB_INSTANCE

        users = {}
        for user_row in conn.execute("SELECT * FROM User"):
            user = User(user_row['name'])
            user.id = user_row['id']
            users[user.id] = user

        publications = {}
        for pub_row in conn.execute("SELECT * FROM Publication"):
            author = users[pub_row['author']]

            pub = Publication(pub_row['title'], author, pub_row['content'])
            pub.id = pub_row['id']
            publications[pub.id] = pub

        for owner2book in conn.execute("SELECT * FROM Owner2Book"):
            owner_id, book_id = owner2book['owner'], owner2book['book']
            users[owner_id].bought_books.append(publications[book_id])

        payments = {}
        for pay_row in conn.execute("SELECT * FROM Payment"):
            from_id, to_id = pay_row['from_'], pay_row['to'],
            payment = Payment(users[from_id], users[to_id], pay_row['quantity'])
            payment.id = pay_row['id']
            payments[payment.id] = payment

        orders = {}
        for order_row in conn.execute('SELECT * FROM "Order"'):
            client_id = order_row['client']
            service_id = order_row['service']
            publication_id = order_row['publication']
            payment_id = order_row['payment']

            client, service = users[client_id], users[service_id]
            publication, payment = publications[publication_id], payments[payment_id]

            order = Order(client, service, publication)
            order.status = order_row['status']
            order.cost = order_row['cost']
            order.payment = order_row['payment']
            order.quantity = order_row['quantity']
            order.id = order_row['id']

            orders[order.id] = order

        return users, publications, payments, orders

    @classmethod
    def close(cls):
        cls.DB_INSTANCE.close()
        cls.DB_INSTANCE = None


class DatabaseEntry(ABC):

    # INSERT INTO Media (id, title, type) VALUES (:id, :title, :type)
    INSERT_STMT_TEMPLATE = "INSERT INTO {table} ({columns}) VALUES ({key_columns})"
    # UPDATE Media SET title=:title, type=:type) WHERE id=:id
    UPDATE_STMT_TEMPLATE = "UPDATE {table} SET {columns2values} WHERE id=:id"

    INSERT_STMT: str
    UPDATE_STMT: str

    def __init__(self):
        self.id = None

    def save(self):
        if self.id is None:
            with Database.DB_INSTANCE as conn:
                self.id = conn.execute(self.INSERT_STMT, self.__dict__).lastrowid
        else:
            with Database.DB_INSTANCE as conn:
                conn.execute(self.UPDATE_STMT, self.__dict__)
