import tkinter as tk
from sha_1 import sha1


class Sha1Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.message = tk.StringVar()
        self.hash = tk.StringVar()

        tk.Label(self, text='SHA-1').grid(row=0, columnspan=3)
        tk.Label(self, text='Сообщение =').grid(row=1, column=0, sticky='e')
        tk.Entry(self, textvariable=self.message).grid(row=1, column=1, sticky='w')
        tk.Button(self, text='Получить хеш-сумму', command=self.calculate_hash).grid(row=1, column=2, sticky='e')
        tk.Label(self, text='Хеш-сумма =').grid(row=2, column=0, sticky='e')
        tk.Entry(self, textvariable=self.hash, width=48).grid(row=2, column=1, sticky='w', columnspan=2)

    def calculate_hash(self):
        self.hash.set(sha1(self.message.get()))
