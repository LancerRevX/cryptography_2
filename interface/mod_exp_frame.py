import tkinter as tk
from lab1 import mod_exp
from tkinter.messagebox import showinfo, showerror


class ModExpFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='Возведение a в степень x по модулю p').grid(row=0, column=0, columnspan=2)

        tk.Label(self, text='a =').grid(column=0, row=1, sticky='e')
        self.a_entry = tk.Entry(self)
        self.a_entry.grid(column=1, row=1, sticky='w')

        tk.Label(self, text='x =').grid(column=0, row=2, sticky='e')
        self.x_entry = tk.Entry(self)
        self.x_entry.grid(column=1, row=2, sticky='w')

        tk.Label(self, text='p =').grid(column=0, row=3, sticky='e')
        self.p_entry = tk.Entry(self)
        self.p_entry.grid(column=1, row=3, sticky='w')

        tk.Button(
            self,
            text='Возвести в степень',
            command=lambda: self.calculate_mod_exp()
        ).grid(column=0, row=4, columnspan=2)

    def calculate_mod_exp(self):
        try:
            result = mod_exp(int(self.a_entry.get()), int(self.x_entry.get()), int(self.p_entry.get()))
            showinfo('Результат', str(result))
        except ValueError:
            #showerror('Ошибка', 'e и z должны быть взаимно простыми')
            pass
