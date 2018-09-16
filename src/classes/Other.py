from enum import Enum


class Payment:

    def __init__(self, from_, to, quantity):
        self.from_ = from_
        self.to = to
        self.quantity = quantity


class Publication:

    class Status(Enum):
        ISSUED = 1
        ACCEPTED = 2
        REJECTED = 3

    def __init__(self, id, title, author, content, status):
        self.id = id
        self.title = title
        self.author = author
        self.content = content
        self.status = status

    def add_to_database(self, db):
        with db.instance as conn:
            c = conn.cursor()
            c.execute("INSERT INTO Publication(title, author, content, status) VALUES (?, ?, ?, ?)",
                      (self.title, self.author.id, self.content, self.status.value))
            self.id = c.lastrowid

    def set_status(self, status, db):
        self.status = status
        with db.instance as conn:
            conn.execute("UPDATE Publication SET status = ? WHERE id = ?", (self.status.value, self.id))

    @classmethod
    def add_to_requests(cls, user, title, file, db):
        with open(file, 'rt') as file:
            book = Publication(None, title, user, file.read(), Publication.Status.ISSUED)
        book.add_to_database(db)
        user.publications.append(book)

    @classmethod
    def get_awaiting_publication(cls, db):
        return [book for book in cls.load_all(db) if book.status is cls.Status.ISSUED]

    @classmethod
    def load_all(cls, db):
        # Получаем список id всех книг
        with db.instance as conn:
            ids = [row['id'] for row in conn.execute("SELECT id FROM Publication")]

        return [cls.load_by_id(id, db) for id in ids]

    @classmethod
    def load_by_id(cls, id, db):
        if db.cache.is_cached(cls.__name__, id):
            return db.cache.get(cls.__name__, id)
        else:
            with db.instance as conn:
                row = conn.execute("SELECT * FROM Publication WHERE id=?", (id,)).fetchone()
                title, content = row['title'], row['content']
                status = cls.Status(row['status'])
                author_lazy = db.lazy(cls_name="User", id=row['author'])

                book = cls(id, title, author_lazy, content, status)

                # Добавляем в кэш (ещё с "ленивыми" полями)
                db.cache.add(cls.__name__, id, book)

                book.author = book.author.load()

            return book


class PrintedBooks:

    def __init__(self, publication, quantity):
        self.publication = publication
        self.quantity = quantity
