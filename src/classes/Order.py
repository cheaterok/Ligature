from enum import Enum


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
