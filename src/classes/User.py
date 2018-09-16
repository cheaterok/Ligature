class User:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.bought_books = []
        self.publications = []

    @property
    def total_owned_books(self):
        return self.bought_books + self.publications

    def get_books_with_status(self, status):
        return [book for book in self.publications if book.status is status]

    def buy_publication(self, publication, db):
        with db.instance as conn:
            conn.execute("INSERT INTO Owner2Book(owner, book) VALUES (?, ?)", (self.id, publication.id))

        self.bought_books.append(publication)

    @classmethod
    def load_by_id(cls, id, db):
        if db.cache.is_cached(cls.__name__, id):
            return db.cache.get(cls.__name__, id)
        else:
            with db.instance as conn:
                row = conn.execute("SELECT * FROM User WHERE id=?", (id,)).fetchone()
                user = cls(id, row['name'])

                for row in conn.execute("SELECT book FROM Owner2Book WHERE owner=?", (id,)):
                    user.bought_books.append(db.lazy(cls_name="Publication", id=row['book']))

                for row in conn.execute("SELECT id FROM Publication WHERE author=?", (id,)):
                    user.publications.append(db.lazy(cls_name="Publication", id=row['id']))

                # Добавляем в кэш (ещё с "ленивыми" полями)
                db.cache.add(cls.__name__, id, user)

                user.bought_books = [lazy.load() for lazy in user.bought_books]
                user.publications = [lazy.load() for lazy in user.publications]

            return user
