from enum import Enum


##############################
#  User and it's subclasses  #
##############################

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


############
#  Orders  #
############

class Order:

    class Status(Enum):
        ISSUED = 1
        CONFIRMED = 2
        PAID = 3

    def __init__(self, client, service, publication):
        self.client = client
        self.service = service
        self.publication = publication

        self.status = self.Status.ISSUED
        self.cost = None
        self.payment = None


class OnlineOrder(Order):
    pass


class PrintingOrder(Order):

    def __init__(self, client, service, publication, quantity):
        super().__init__(client, service, publication)
        self.quantity = quantity


####################
#  Other entities  #
####################

class Payment:

    def __init__(self, _from, to, quantity):
        self._from = _from
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
