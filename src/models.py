from pathlib import Path

from pony.orm import Database, Required, Set


db = Database()


class User(db.Entity):
    name = Required(str)
    publications = Set('Publication', reverse='author')
    owned_books = Set('Publication', reverse='owners')


class Publication(db.Entity):
    title = Required(str)
    author = Required(User, reverse='publications')
    owners = Set(User, reverse='owned_books')
    content = Required(str)
    status = Required(int)


DB_FILE = Path.cwd() / "resources" / "orm_database.sqlite3"

db.bind(provider='sqlite', filename=str(DB_FILE), create_db=True)
db.generate_mapping(create_tables=True)
