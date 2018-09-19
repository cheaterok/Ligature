import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from database import Database
from classes import User


class UserJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if not isinstance(o, User):
            return super().default(o)
        else:
            return {
                'id': o.id,
                'name': o.name,
                'bought books': [book.title for book in o.bought_books],
                'publications': [book.title for book in o.publications]
            }


class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        self.wfile.write(USER_JSON_BYTES)


if __name__ == '__main__':
    with Database() as db:
        user = User.load_by_id(1, db)

    USER_JSON_BYTES = bytes(json.dumps(user, cls=UserJSONEncoder), encoding='utf-8')

    address = ('', 8000)
    server = HTTPServer(address, Handler)

    server.serve_forever()
