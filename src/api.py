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


@hug.get("/get_reader_data")
@db_session
def get_reader_data(username: hug.types.text):
    "Перечисляет все книги, доступные для покупки пользователем."
    current_user = select(user for user in User if user.name == username).first()

    if not current_user:
        current_user = User(name=username)
        commit()
    
    owned_books = select(book for book in Publication if book in current_user.owned_books or
                                                      book in current_user.publications)
    available_books = select(book for book in Publication
                                if book not in current_user.owned_books and 
                                book not in current_user.publications and
                                book.status == 1)
    return {
        'id': current_user.id,
        'owned_books': [book.title for book in owned_books],
        'available_books': [book.title for book in available_books]
        }

@hug.get("/get_writer_data")
@db_session
def get_writer_data(username: hug.types.text):
    "Перечисляет все книги, доступные для покупки пользователем."
    current_user = select(user for user in User if user.name == username).first()
    
    all_books = select(book for book in Publication if book in current_user.publications)

    published_books = [book.title for book in all_books if book.status == 1]
    awaiting_books = [book.title for book in all_books if book.status == 2]
    rejected_books = [book.title for book in all_books if book.status == 3]

    return {
        'id': current_user.id,
        'published_books': published_books,
        'awaiting_books': awaiting_books,
        'rejected_books': rejected_books
        }

@hug.get("/get_publisher_data")
@db_session
def get_publisher_data(username: hug.types.text):
    "Перечисляет все книги, доступные для покупки пользователем."
    current_user = select(user for user in User if user.name == username).first()
    
    awaiting_books = select(book for book in Publication if book.status == 2)


    return {
        'id': current_user.id,
        'awaiting_books': [book.title for book in awaiting_books]
        }

@hug.get("/buy_book")
@db_session
def buy_book(username: hug.types.text, title: hug.types.text):
        user = select(user for user in User if user.name == username).first()
        book = select(book for book in Publication if book.title == title).first()

        user.owned_books.add(book)

        return {
                "owned_books": user.owned_books
        }

@hug.post("/publish_book")
@db_session
def publish_book(body):
        user = select(user for user in User if user.name == body['username']).first()

        new_book = Publication(
                title=body['title'],
                author=user,
                content=body['content'],
                status=2
        )

        print(new_book.title, new_book.content)

@hug.get("/accept_book")
@db_session
def accept_book(title: hug.types.text):
        book = select(book for book in Publication if book.title == title).first()
        book.status = 1

@hug.get("/reject_book")
@db_session
def reject_book(title: hug.types.text):
        book = select(book for book in Publication if book.title == title).first()
        book.status = 3
