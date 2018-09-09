class User:

    def __init__(self, name):
        self.name = name


class Reader(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bought_books = []


class Writer(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publications = []


class Publisher(User):
    pass
