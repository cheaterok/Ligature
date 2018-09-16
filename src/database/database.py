import sqlite3
from pathlib import Path
from weakref import WeakValueDictionary

import classes


class Database:

    NAME = "database.sqlite3"
    FOLDER = Path.cwd()
    PATH = FOLDER/"resources"/NAME

    INIT_SCRIPT = Path.cwd()/"resources"/"init_script.sql"

    def __init__(self, db_path=None):
        self.instance = None
        if db_path is not None:
            self.path = db_path
        else:
            self.path = self.PATH

        self.cache = Cache()

    def open(self):
        # If using in-memory DB or DB file does not exist - create DB
        if self.path == ":memory:" or not self.path.exists():
            self.instance = sqlite3.connect(self.path)
            with self.instance as conn:
                with open(self.INIT_SCRIPT, 'rt') as sql_file:
                    conn.executescript(sql_file.read())
        else:
            self.instance = sqlite3.connect(self.path)

        self.instance.row_factory = sqlite3.Row

    def is_initialised(self):
        return bool(self.instance)

    def close(self):
        self.instance.close()
        self.instance = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def lazy(self, cls_name, id):
        return Lazy(cls_name, id, self)


class Lazy:

    def __init__(self, cls_name, id, db):
        self.cls = getattr(classes, cls_name)
        self.id = id
        self._db = db

    def load(self):
        return self.cls.load_by_id(self.id, self._db)


class Cache:

    def __init__(self):
        self._dict = WeakValueDictionary()

    @staticmethod
    def key_func(cls_name, id):
        return f"{cls_name}:{id}"

    def is_cached(self, cls_name, id):
        return self.key_func(cls_name, id) in self._dict

    def add(self, cls_name, id, value):
        self._dict[self.key_func(cls_name, id)] = value

    def get(self, cls_name, id):
        return self._dict[self.key_func(cls_name, id)]
