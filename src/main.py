from pathlib import Path

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

from database import Database
from classes import User, Publication


DATABASE = None

# Вся необходимая текущая информация в приложении
# Чтобы не таскать её по окошкам
CURRENT_INFO = {}


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = Style()
        self.style.theme_use("clam")
        self.cur_window = None
        self.switch_window(LoginWindow(self))

    def switch_window(self, window):
        if self.cur_window is not None:
            self.cur_window.destroy()
        self.cur_window = window
        self.wm_title(self.cur_window.TITLE)
        self.pack()

    def pack(self):
        self.cur_window.pack()


class LoginWindow(Frame):

    TITLE = "Окно входа"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_1 = Label(self, text="Я: ")

        self.choice_var = StringVar(self)
        self.choice_reader = Radiobutton(self, text='Читатель', variable=self.choice_var, value='Читатель')
        self.choice_writer = Radiobutton(self, text='Писатель', variable=self.choice_var, value='Писатель')
        self.choice_publisher = Radiobutton(self, text='Издатель', variable=self.choice_var, value='Издатель')

        self.label_2 = Label(self, text="Мой ID: ")

        self.entry_data = StringVar(self)
        self.entry = Entry(self, textvariable=self.entry_data)

        self.login_btn = Button(self, text="Войти", command=self.login)

    def pack(self):
        super().pack()
        self.label_1.pack()
        self.choice_reader.pack()
        self.choice_writer.pack()
        self.choice_publisher.pack()
        self.label_2.pack()
        self.entry.pack()
        self.login_btn.pack()

    def login(self):
        role = self.choice_var.get()
        id = self.entry_data.get()
        if role and id:
            CURRENT_INFO['user'] = User.load_by_id(id, DATABASE)
            CURRENT_INFO['role'] = role

            if role == "Читатель":
                self.master.switch_window(ReaderWindow(self.master))
            if role == "Писатель":
                self.master.switch_window(WriterWindow(self.master))
            if role == "Издатель":
                self.master.switch_window(PublisherWindow(self.master))


# Список с названием и прокруткой
class ListboxFrame(Frame):

        class ListboxWithScroll(Frame):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.listbox = Listbox(self, height=10)
                self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.listbox.yview)
                self.listbox['yscrollcommand'] = self.scrollbar.set

                self.curselection = self.listbox.curselection
                self.insert = self.listbox.insert
                self.delete = self.listbox.delete

            def pack(self):
                super().pack()
                self.listbox.pack(side=LEFT, expand=True, fill=BOTH)
                self.scrollbar.pack(side=RIGHT, expand=True, fill=BOTH)

        def __init__(self, *args, label=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.label = Label(self, text=label)
            self.listbox = self.ListboxWithScroll(self)
            self.button = None  # Можно задать кнопку снаружи после создания окна

        def get_selected_idx(self):
            cur_id = self.listbox.curselection()
            # Возвращает tuple(где первый элемент - индекс)
            return cur_id[0] if cur_id else None

        def set_books(self, books):
            # В ListBox ничего кроме названий книг не вставляется
            self.listbox.delete(0, END)
            for book in books:
                self.listbox.insert(END, book.title)

        def pack(self, *args, **kwargs):
            super().pack(*args, **kwargs)
            self.label.pack()
            self.listbox.pack()
            if self.button is not None:
                self.button.pack()


#################
# Окна Читателя #
#################

class ReaderWindow(Frame):

    TITLE = "Окно Читателя"

    class LabelFrame(Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            user = CURRENT_INFO['user']
            self.label_id = Label(self, text=f"ID: {user.id}")
            self.label_name = Label(self, text=f"Имя: {user.name}")

        def pack(self, *args, **kwargs):
            super().pack(*args, **kwargs)
            self.label_id.pack(side=TOP, anchor=W)
            self.label_name.pack(side=BOTTOM, anchor=W)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = CURRENT_INFO['user']

        self.label_frame = self.LabelFrame(self)

        self.list_books_owned = ListboxFrame(self, label="Купленные книги")
        self.list_books_owned.set_books(user.total_owned_books)

        self.list_books_all = ListboxFrame(self, label="Магазин")

        # Сохраним на всякий случай
        CURRENT_INFO['All Publications'] = Publication.load_all(DATABASE)

        # Не показываем пользователю уже имеющиеся у него книги
        CURRENT_INFO['Books in Store'] = list(set(CURRENT_INFO['All Publications']) - set(user.total_owned_books))

        self.list_books_all.set_books(CURRENT_INFO['Books in Store'])

        self.buy_selected_btn = Button(self, text="Купить книгу", command=self.buy_book)

    def pack(self):
        super().pack()
        self.label_frame.pack(side=LEFT)
        self.list_books_owned.pack(side=LEFT)
        self.list_books_all.pack(side=LEFT)
        self.buy_selected_btn.pack(side=LEFT)

    def buy_book(self):
        cur_book_idx = self.list_books_all.get_selected_idx()
        # Ничего не делать, если ничего не выделено
        if cur_book_idx is None:
            return
        cur_book = CURRENT_INFO['Books in Store'][cur_book_idx]
        self.master.switch_window(OrderWindow(self.master, publication=cur_book))


class OrderWindow(Frame):

    TITLE = "Окно заказа"

    def __init__(self, *args, publication=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.publication = publication
        title, author, price = publication.title, publication.author, 500
        self.label_title = Label(self, text=f"Наименование: {title}")
        self.label_author = Label(self, text=f"Автор: {author.name}")
        self.label_price = Label(self, text=f"Цена: {price}")

        self.label_progress = Label(self, text="Производится поиск...")
        self.progress_bar = Progressbar(self, orient=HORIZONTAL, length=100, mode='indeterminate')
        self.buy_button = Button(self, text="Купить", state=DISABLED, command=self.buy_book)

    def after_progress_bar(self):
        self.progress_bar.stop()
        self.buy_button['state'] = ACTIVE
        self.label_progress['text'] = "Издание найдено!"

    def buy_book(self):
        CURRENT_INFO['user'].buy_publication(self.publication, DATABASE)
        messagebox.showinfo(message="Издание добавлено в вашу библиотеку!")
        self.master.switch_window(ReaderWindow(self.master))

    def pack(self):
        super().pack()
        self.label_title.pack(anchor=W)
        self.label_author.pack(anchor=W)
        self.label_price.pack(anchor=W)

        self.label_progress.pack()
        self.progress_bar.pack()
        self.buy_button.pack()

        # Добавляем в pack не относящуюся к нему логику
        # Т.к. только он вызывается при переходе между окнами
        # А педалить логику инициализации нового окна лень
        self.progress_bar.start(interval=10)
        self.progress_bar.after(1000, self.after_progress_bar)


#################
# Окна Писателя #
#################

class WriterWindow(Frame):

    TITLE = "Окно Писателя"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.list_published = ListboxFrame(self, label="Опубликованные")
        self.list_published.button = Button(self.list_published, text="Заказать печать", command=self.order_print)
        self.list_published.set_books(CURRENT_INFO['user'].get_books_with_status(Publication.Status.ACCEPTED))

        self.list_waiting = ListboxFrame(self, label="Ожидающие решения")
        self.list_waiting.button = Button(self.list_waiting, text="Опубликовать новую", command=self.publish_new)
        self.list_waiting.set_books(CURRENT_INFO['user'].get_books_with_status(Publication.Status.ISSUED))

        self.list_rejected = ListboxFrame(self, label="Отказано в публикации")
        self.list_rejected.set_books(CURRENT_INFO['user'].get_books_with_status(Publication.Status.REJECTED))

    def order_print(self):
        raise NotImplementedError

    def publish_new(self):
        self.master.switch_window(NewPublicationWindow(self.master))

    def pack(self):
        super().pack()
        self.list_published.pack(side=LEFT)
        self.list_waiting.pack(side=LEFT)
        self.list_rejected.pack(side=LEFT, anchor=N)


class NewPublicationWindow(Frame):

    TITLE = "Новая публикация"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name_frame = Frame(self)
        self.name_frame.data = StringVar(self.name_frame)
        self.name_frame.label = Label(self.name_frame, text="Название")
        self.name_frame.entry = Entry(self.name_frame, textvariable=self.name_frame.data)

        self.file_frame = Frame(self)
        self.file_frame.data = StringVar(self.file_frame)
        self.file_frame.label = Label(self.file_frame, text="Файл")
        self.file_frame.entry = Entry(self.file_frame, textvariable=self.file_frame.data)
        self.btn_image = PhotoImage(file=str(Path("resources")/"folder.png"))
        self.file_frame.filedialog_btn = Button(self.file_frame, image=self.btn_image, command=self.open_file_dialog)

        self.publish_btn = Button(self, text="Отправить", command=self.publish)

    def open_file_dialog(self):
        self.file_frame.data.set(askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*"))))

    def publish(self):
        title = self.name_frame.data.get()
        file = self.file_frame.data.get()
        # Если что-то не заполнено - ничего не делать
        if not (title and file):
            return

        Publication.add_to_requests(CURRENT_INFO['user'], title, file, DATABASE)

        messagebox.showinfo(message="Публикация добавлена!")
        self.master.switch_window(WriterWindow(self.master))

    def pack(self):
        super().pack()
        self.name_frame.pack(expand=True, fill=X)
        self.name_frame.label.pack(side=LEFT, anchor=W)
        self.name_frame.entry.pack(side=RIGHT, expand=True, fill=X, anchor=E)

        self.file_frame.pack(expand=True, fill=X)
        self.file_frame.label.pack(side=LEFT, anchor=W)
        self.file_frame.entry.pack(side=LEFT, anchor=E)
        self.file_frame.filedialog_btn.pack()

        self.publish_btn.pack(side=BOTTOM)


#################
# Окна Издателя #
#################

class PublisherWindow(Frame):

    TITLE = "Окно Издателя"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_requested_publications = ListboxFrame(self, label="Запросы на публикацию:")

        self.update_list()

        self.btns_frame = Frame(self)
        self.btns_frame.accept_btn = Button(self.btns_frame, text="Подтвердить",
                                            command=lambda: self.set_status(Publication.Status.ACCEPTED))
        self.btns_frame.reject_btn = Button(self.btns_frame, text="Отказать",
                                            command=lambda: self.set_status(Publication.Status.REJECTED))

    def set_status(self, status):
        book_idx = self.list_requested_publications.get_selected_idx()
        if book_idx is None:
            return
        book = CURRENT_INFO['Awaiting Acceptance'][book_idx]
        book.set_status(status, DATABASE)
        self.update_list()

    def update_list(self):
        CURRENT_INFO['Awaiting Acceptance'] = Publication.get_awaiting_publication(DATABASE)
        self.list_requested_publications.set_books(CURRENT_INFO['Awaiting Acceptance'])

    def pack(self):
        super().pack()
        self.list_requested_publications.pack()
        self.btns_frame.pack()
        self.btns_frame.accept_btn.pack(side=LEFT)
        self.btns_frame.reject_btn.pack(side=LEFT)


if __name__ == '__main__':
    DATABASE = Database()
    with DATABASE:
        # Инициализация GUI
        app = Application()
        app.pack()
        app.mainloop()
