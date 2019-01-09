import hug
from pony.orm import db_session, select, commit

from models import User, Publication


@hug.local()
@db_session
def create_user(username):
    "Создаёт пользователя с указанным именем."
    new_user = User(name=username)
    commit()  # Нужно закоммитить, чтобы получить id
    return {'id': new_user.id}

@hug.get("/login")
@db_session
def login(username: hug.types.text):
    user = select(user for user in User if user.name == username).first()
    return {'id': user.id, 'name': user.name}

@hug.local()
@db_session
def list_available_books(user_id):
    "Перечисляет все книги, доступные для покупки пользователем."
    current_user = User[user_id]
    available_books = select(book for book in Publication
                                if book not in current_user.owned_books and 
                                book not in current_user.publications)
    return {'books': {'title': book.title for book in available_books}}

@hug.local()
def buy_book(user_id, book_id):
    "Добавляет книгу в список купленных пользователем."

@hug.local()
@db_session
def upload_book(user_id, title, content):
    "Загружает книгу от имени пользователя."
    book = Publication(title=title, author=User[user_id], content=content, status=1)
    return book.__dict__

@hug.local()
def review_book(user_id, book_id, answer):
    "Оставляет вердикт по книге от имени издателя."
