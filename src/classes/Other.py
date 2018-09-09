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

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
        self.status = self.Status.ISSUED


class PrintedBooks:

    def __init__(self, publication, quantity):
        self.publication = publication
        self.quantity = quantity
