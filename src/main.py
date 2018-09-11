from tkinter import *
from tkinter.ttk import *


class Application(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.login_window = LoginWindow(master=self)
        self.login_window = ReaderWindow(self, id=123, name="Петр Петрович")

    def pack(self):
        super().pack()
        self.login_window.pack()


class LoginWindow(Frame):

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
        print(role, id)


class ReaderWindow(Frame):

    class LabelFrame(Frame):
        def __init__(self, *args, id=None, name=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.label_id = Label(self, text=f"ID: {id}")
            self.label_name = Label(self, text=f"Имя: {name}")

        def pack(self, *args, **kwargs):
            super().pack(*args, **kwargs)
            self.label_id.pack(side=TOP, anchor=W)
            self.label_name.pack(side=BOTTOM, anchor=W)

    class ListboxFrame(Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.listbox = Listbox(self, height=10)
            self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.listbox.yview)
            self.listbox['yscrollcommand'] = self.scrollbar.set

        def get_selected(self):
            return self.listbox.get(self.listbox.curselection())

        def set_items(self):
            for i in range(1, 101):
                self.listbox.insert('end', 'Line %d of 100' % i)

        def bind(self, *args, **kwargs):
            # Специально не вызываем super()
            # Предполагается, что bind пользователь хочет вызвать только для ListBox
            self.listbox.bind(*args, **kwargs)

        def pack(self, *args, **kwargs):
            super().pack(*args, **kwargs)
            self.listbox.pack(side=LEFT, expand=True, fill=BOTH)
            self.scrollbar.pack(side=RIGHT, expand=True, fill=BOTH)

    def __init__(self, *args, id=None, name=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_frame=self.LabelFrame(self, id=id, name=name)

        self.list_books_owned = self.ListboxFrame(self)
        self.list_books_owned.set_items()

        self.list_books_all = self.ListboxFrame(self)
        self.list_books_all.set_items()

        self.buy_selected_btn = Button(self, text="Купить книгу", command=self.buy_book, state=DISABLED)

        def enable_btn(event):
            self.buy_selected_btn['state'] = NORMAL

        self.list_books_all.bind('<<ListboxSelect>>', enable_btn)

    def pack(self):
        super().pack()
        self.label_frame.pack(side=LEFT)
        self.list_books_owned.pack(side=LEFT)
        self.list_books_all.pack(side=LEFT)
        self.buy_selected_btn.pack(side=LEFT)

    def buy_book(self):
        print(self.list_books_all.get_selected())


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.pack()
    app.mainloop()
