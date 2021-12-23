import tkinter as tk
from tkinter.messagebox import showerror, showwarning
from elgamal_encryption import *


class ElgamalFrame(tk.Frame):
    ERROR_TITLE = 'Ошибка'
    ERROR_MESSAGES: dict[type(ElgamalError)] = {
        InvalidPOrderError: 'Порядок p должен быть положительным целым числом',
        InvalidPError: 'p должно быть простым числом',
        InvalidGError: 'g должно быть первообразным корнем p',
        InvalidPrivateKeyError: 'c должно находиться в интервале (1, p-1)',
        InvalidPublicKeyError: 'd должно находиться в интервале [1, p)',
        InvalidMessageError: 'm должно быть натуральным числом меньше p',
        InvalidEncryptedMessageError: 'e и r должны быть натуральными числами меньше p',
        InvalidKError: 'k должно быть целым числом больше 1 и меньше p - 1'
    }
    GENERATE_BUTTON_TEXT = 'Генерировать'

    def __init__(self, master):
        super().__init__(master)

        self.m = tk.IntVar()
        self.p = tk.IntVar()
        self.p_order = tk.IntVar()
        self.g = tk.IntVar()
        self.c = tk.IntVar()
        self.d = tk.IntVar()
        self.e = tk.IntVar()
        self.r = tk.IntVar()
        self.k = tk.IntVar()

        p_frame = tk.Frame(self)
        tk.Label(p_frame, text='p =').pack(side='left')
        tk.Entry(p_frame, textvariable=self.p).pack(side='left')
        tk.Label(p_frame, text='Порядок').pack(side='left')
        tk.Entry(p_frame, textvariable=self.p_order).pack(side='left')
        tk.Button(p_frame, text=self.GENERATE_BUTTON_TEXT, command=self.generate_p).pack(side='left')
        p_frame.pack()

        g_frame = tk.Frame(self)
        tk.Label(g_frame, text='g =').pack(side='left')
        tk.Entry(g_frame, textvariable=self.g).pack(side='left')
        tk.Button(g_frame, text=self.GENERATE_BUTTON_TEXT, command=self.generate_g).pack(side='left')
        g_frame.pack()

        c_frame = tk.Frame(self)
        tk.Label(c_frame, text='c =').pack(side='left')
        tk.Entry(c_frame, textvariable=self.c).pack(side='left')
        tk.Button(c_frame, text=self.GENERATE_BUTTON_TEXT, command=self.generate_c).pack(side='left')
        c_frame.pack()

        d_frame = tk.Frame(self)
        tk.Label(d_frame, text='d =').pack(side='left')
        tk.Entry(d_frame, textvariable=self.d).pack(side='left')
        tk.Button(d_frame, text='Рассчитать', command=self.get_d).pack(side='left')
        d_frame.pack()

        k_frame = tk.Frame(self)
        tk.Label(k_frame, text='k =').pack(side='left')
        tk.Entry(k_frame, textvariable=self.k).pack(side='left')
        tk.Button(k_frame, text=self.GENERATE_BUTTON_TEXT, command=self.generate_k).pack(side='left')
        k_frame.pack()

        message_frame = tk.LabelFrame(self, text='Незашифрованное сообщение')
        tk.Label(message_frame, text='m =').pack(side='left')
        tk.Entry(message_frame, textvariable=self.m).pack(side='left')
        tk.Button(message_frame, text='Зашифровать', command=self.encrypt_message).pack(side='left')
        message_frame.pack()

        encrypted_message_frame = tk.LabelFrame(self, text='Зашифрованное сообщение')
        tk.Label(encrypted_message_frame, text='r =').pack(side='left')
        tk.Entry(encrypted_message_frame, textvariable=self.r).pack(side='left')
        tk.Label(encrypted_message_frame, text='e =').pack(side='left')
        tk.Entry(encrypted_message_frame, textvariable=self.e).pack(side='left')
        tk.Button(encrypted_message_frame, text='Расшифровать', command=self.decrypt_message).pack(side='left')
        encrypted_message_frame.pack()

    def encrypt_message(self):
        try:
            r, e = encrypt(self.m.get(), self.p.get(), self.g.get(), self.d.get(), self.k.get())
            self.r.set(r)
            self.e.set(e)
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])

    def decrypt_message(self):
        try:
            self.m.set(decrypt((self.r.get(), self.e.get()), self.p.get(), self.c.get()))
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])

    def generate_p(self):
        try:
            self.p.set(generate_p(self.p_order.get()))
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])

    def generate_g(self):
        try:
            self.g.set(generate_g(self.p.get(), self.g.get()))
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])

    def generate_c(self):
        try:
            c = generate_private_key(self.p.get())
            if c is None:
                showwarning(self.ERROR_TITLE, 'Не удалось сгенерировать c')
            else:
                self.c.set(c)
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])

    def generate_k(self):
        try:
            self.k.set(generate_k(self.p.get()))
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])

    def get_d(self):
        try:
            self.d.set(get_public_key(self.p.get(), self.g.get(), self.c.get()))
        except ElgamalError as error:
            showerror(self.ERROR_TITLE, self.ERROR_MESSAGES[type(error)])