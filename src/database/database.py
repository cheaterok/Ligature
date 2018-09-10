import sqlite3
from pathlib import Path


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

        cls.DB_INSTANCE = sqlite3.connect(cls.DB_PATH)

        # If using in-memory DB or DB file does not exist - create DB
        if cls.DB_PATH == ":memory:" or not cls.DB_PATH.exists():
            with cls.DB_INSTANCE as conn:
                with open(cls.INIT_SCRIPT, 'rt') as sql_file:
                    conn.executescript(sql_file.read())

        cls.DB_INSTANCE.row_factory = sqlite3.Row

    @classmethod
    def is_initialised(cls):
        return bool(cls.DB_INSTANCE)

    @classmethod
    def close(cls):
        cls.DB_INSTANCE.close()
        cls.DB_INSTANCE = None
