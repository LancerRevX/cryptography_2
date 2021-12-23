import tkinter as tk
from md5 import md5


class Md5Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.message = tk.StringVar()
        self.hash = tk.StringVar()

        tk.Label(self, text='Сообщение =').grid(row=0, column=0, sticky='e')
        tk.Entry(self, textvariable=self.message).grid(row=0, column=1, sticky='w')
        tk.Button(self, text='Получить хеш-сумму', command=self.calculate_hash).grid(row=1, column=0, columnspan=2)
        tk.Label(self, text='Хеш-сумма =').grid(row=2, column=0, sticky='e')
        tk.Entry(self, textvariable=self.hash, width=32).grid(row=2, column=1, sticky='w')

    def calculate_hash(self):
        self.hash.set(md5(self.message.get()))
