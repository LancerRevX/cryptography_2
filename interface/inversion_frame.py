import tkinter as tk
from lab1 import inversion
from tkinter.messagebox import showinfo, showerror


class InversionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='Инверсия e по модулю z').grid(row=0, column=0, columnspan=2)

        tk.Label(self, text='e = ').grid(column=0, row=1)
        self.e_entry = tk.Entry(self)
        self.e_entry.grid(column=1, row=1)

        tk.Label(self, text='z = ').grid(column=0, row=2)
        self.z_entry = tk.Entry(self)
        self.z_entry.grid(column=1, row=2)

        tk.Button(
            self,
            text='Найти инверсию',
            command=lambda: self.calculate_inversion()
        ).grid(column=0, row=3, columnspan=2)

    def calculate_inversion(self):
        try:
            result = inversion(int(self.e_entry.get()), int(self.z_entry.get()))
            showinfo('Результат', str(result))
        except ValueError:
            showerror('Ошибка', 'e и z должны быть взаимно простыми')
