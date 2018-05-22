from classes import User, Reader, Writer, Publisher,\
                     Order, OnlineOrder, PrintingOrder,\
                     Publication, Payment, PrintedBooks


class State:

    def __init__(self):
        self.users = []
        self.orders = []


def create_user(state: State, user_type: User, name: str):
    state.users.append(user_type(name))


def create_order(state: State, order_type: Order, *args: [str]):
    client_id, service_id, publication_id = map(int, args[:3])

    client, service = state.get_user_by_id(client_id), state.get_user_by_id(service_id)
    publication = state.get_publication_by_id(publication_id)

    if order_type is PrintingOrder:
        quantity = int(args[3])
        order = order_type(client, service, publication, quantity)
    else:
        order = order_type(client, service, publication)

    state.orders.append(order)
    

def confirm_order(state: State, order_id: str):
    order = state.get_order_by_id(int(order_id))
    order.status = order.Status.CONFIRMED


def review_publication(state: State, publication_id: str, status_str: str):
    publication = state.get_publication_by_id(int(publication_id))
    publication.status = publication.Status[status_str]


class Commander:

    ACTIONS = {
        "create": {
            "reader": lambda state, name: create_user(state, Reader, name),
            "writer": lambda state, name: create_user(state, Writer, name),
            "publisher": lambda state, name: create_user(state, Publisher, name),
            "online_order": lambda state, *args: create_order(state, OnlineOrder, *args),
            "printing_order": lambda state, *args: create_order(state, PrintingOrder, *args)
        },
        "confirm": {
            "order": confirm_order
        },
        "review": {
            "publication": review_publication
        }
    }

    def __init__(self):
        self.state = State()

    def process(self, command):
        action, entity, *args = command.split()
        function = self.ACTIONS[action][entity]
        function(self.state, *args)
