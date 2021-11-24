import tkinter as tk
from diffie_hellman import calculate_secret_key, generate_g, generate_q
from rsa import exceptions
from tkinter.messagebox import showerror


class DiffieHellmanFrame(tk.Frame):
    P_LABEL_TEXT = 'p = 2*q + 1 = '

    def __init__(self, master):
        super().__init__(master)

        self.q = tk.IntVar(value=2)
        self.q.trace_add('write', lambda *args: self.p.set(self.q.get()*2 + 1))
        self.p = tk.IntVar(value=self.q.get()*2 + 1)
        self.p.trace_add('write', lambda *args: self.p_text.set(f'{self.P_LABEL_TEXT}{self.p.get()}'))
        self.p_text = tk.StringVar(value=f'{self.P_LABEL_TEXT}{self.p.get()}')
        self.g = tk.IntVar(value=1)
        self.a = tk.IntVar(value=1)
        self.b = tk.IntVar(value=1)
        self.B = tk.IntVar(value=0)
        self.A = tk.IntVar(value=0)
        self.K = tk.IntVar(value=0)

        tk.Label(self, text='q = ').grid(row=0, column=0)
        self.q_entry = tk.Entry(self, textvariable=self.q)
        self.q_entry.grid(row=0, column=1)
        tk.Button(self, text='Генерировать', command=self.generate_q).grid(row=0, column=2)

        self.p_label = tk.Label(self, textvariable=self.p_text)
        self.p_label.grid(row=1, column=1)

        tk.Label(self, text='g = ').grid(row=2, column=0)
        self.g_entry = tk.Entry(self, textvariable=self.g)
        self.g_entry.grid(row=2, column=1)
        tk.Button(self, text='Генерировать', command=self.generate_g).grid(row=2, column=2)

        tk.Label(self, text='a = ').grid(row=3, column=0)
        self.a_entry = tk.Entry(self, textvariable=self.a)
        self.a_entry.grid(row=3, column=1)

        tk.Label(self, text='b = ').grid(row=4, column=0)
        self.b_entry = tk.Entry(self, textvariable=self.b)
        self.b_entry.grid(row=4, column=1)

        tk.Button(
            self,
            text='Рассчитать секретный ключ K',
            command=self.calculate_secret_key
        ).grid(row=5, column=0, columnspan=2)

        tk.Label(self, text='A = ').grid(row=6, column=0)
        self.A_label = tk.Label(self, textvariable=self.A)
        self.A_label.grid(row=6, column=1, sticky=tk.W)

        tk.Label(self, text='B = ').grid(row=7, column=0)
        self.B_label = tk.Label(self, textvariable=self.B)
        self.B_label.grid(row=7, column=1, sticky=tk.W)

        tk.Label(self, text='K = ').grid(row=8, column=0)
        self.K_label = tk.Label(self, textvariable=self.K)
        self.K_label.grid(row=8, column=1, sticky=tk.W)

    def calculate_secret_key(self):
        try:
            A, B, K = calculate_secret_key(self.g.get(), self.p.get(), self.a.get(), self.b.get())
            self.A.set(A)
            self.B.set(B)
            self.K.set(K)
        except exceptions.NumberNotPrimeError:
            showerror('Ошибка', 'q и p должны быть простыми числами')
        except exceptions.NumberNotNaturalError:
            showerror('Ошибка', 'a и b должны быть натуральными числами')
        except ValueError:
            showerror('Ошибка', 'Некорректное значение g')

    def generate_q(self):
        try:
            self.q.set(generate_q(self.q.get()))
        except exceptions.NumberNotPrimeError:
            showerror('Ошибка', 'Начальное q должно быть простым')

    def generate_g(self):
        try:
            g = generate_g(self.q.get(), self.g.get())
            if g is None:
                showerror('Ошибка', 'Не удалось сгенерировать g')
            else:
                self.g.set(g)
        except exceptions.NumberNotPrimeError:
            showerror('Ошибка', 'q и p должны быть простыми числами')
