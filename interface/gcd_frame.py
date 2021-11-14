import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from lab1 import gcd


class GcdFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='Первое число').grid(column=0, row=0)
        self.first_entry = tk.Entry(self)
        self.first_entry.grid(column=1, row=0)

        tk.Label(self, text='Второе число').grid(column=0, row=1)
        self.second_entry = tk.Entry(self)
        self.second_entry.grid(column=1, row=1)

        tk.Button(
            self,
            text='Найти НОД',
            command=lambda: self.calculate_gcd()
        ).grid(column=0, row=2, columnspan=2)

    def calculate_gcd(self):
        try:
            result = gcd(int(self.first_entry.get()), int(self.second_entry.get()))
            showinfo('Результат', str(result[0]))
        except ValueError:
            showerror('Ошибка', 'Оба числа должны быть натуральными')
