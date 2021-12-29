import tkinter as tk
from rsa import create_keys, encode_text, exceptions, generate_e
from tkinter.messagebox import showerror


class RsaFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        create_key_frame = tk.Frame(self)
        self.p = tk.IntVar(value=599)
        tk.Label(create_key_frame, text='p =').grid(row=0, column=0, sticky='e')
        tk.Entry(create_key_frame, textvariable=self.p).grid(row=0, column=1)

        self.q = tk.IntVar(value=5)
        tk.Label(create_key_frame, text='q =').grid(row=1, column=0, sticky='e')
        tk.Entry(create_key_frame, textvariable=self.q).grid(row=1, column=1)

        self.e = tk.IntVar(value=3)
        tk.Label(create_key_frame, text='e =').grid(row=2, column=0, sticky='e')
        tk.Entry(create_key_frame, textvariable=self.e).grid(row=2, column=1)
        tk.Button(create_key_frame, text='Генерировать e', command=self.generate_e).grid(row=2, column=2)

        tk.Button(create_key_frame, text='Создать пару ключей', command=self.create_keys).grid(row=3, columnspan=3)
        create_key_frame.pack(pady=(16, 16))

        encrypt_frame = tk.Frame(self)
        self.public_key = (tk.IntVar(), tk.IntVar())
        tk.Label(encrypt_frame, text='Открытый ключ').grid(row=1, column=0)
        tk.Label(encrypt_frame, text='e =').grid(row=1, column=1)
        tk.Entry(encrypt_frame, textvariable=self.public_key[0]).grid(row=1, column=2)
        tk.Label(encrypt_frame, text='n =').grid(row=1, column=3)
        tk.Entry(encrypt_frame, textvariable=self.public_key[1]).grid(row=1, column=4)

        tk.Label(encrypt_frame, text='Текст').grid(row=2, columnspan=5)
        self.text = tk.Text(encrypt_frame, height=8, width=32)
        self.text.grid(row=3, columnspan=5)

        tk.Button(encrypt_frame, text='Зашифровать текст', command=self.encrypt).grid(row=4, columnspan=5)
        encrypt_frame.pack(pady=(0, 16))

        decrypt_frame = tk.Frame(self)
        self.private_key = (tk.IntVar(), tk.IntVar())
        tk.Label(decrypt_frame, text='Закрытый ключ').grid(row=1, column=0)
        tk.Label(decrypt_frame, text='d =').grid(row=1, column=1)
        tk.Entry(decrypt_frame, textvariable=self.private_key[0]).grid(row=1, column=2)
        tk.Label(decrypt_frame, text='n =').grid(row=1, column=3)
        tk.Entry(decrypt_frame, textvariable=self.private_key[1]).grid(row=1, column=4)

        tk.Label(decrypt_frame, text='Текст').grid(row=2, columnspan=5)
        self.encrypted_text = tk.Text(decrypt_frame, height=8, width=32)
        self.encrypted_text.grid(row=3, columnspan=5)

        tk.Button(decrypt_frame, text='Расшифровать текст', command=self.decrypt).grid(row=4, columnspan=5)
        decrypt_frame.pack(pady=(0, 16))

    def create_keys(self):
        try:
            public_key, private_key = create_keys(self.p.get(), self.q.get(), self.e.get())
            self.public_key[0].set(public_key[0])
            self.public_key[1].set(public_key[1])
            self.private_key[0].set(private_key[0])
            self.private_key[1].set(private_key[1])
        except exceptions.NumberNotNaturalError:
            showerror('Ошибка', 'p и q должны быть натуральными')
        except exceptions.NumberNotPrimeError:
            showerror('Ошибка', 'p и q должны быть простыми')
        except exceptions.InvalidPublicExponentError:
            showerror('Ошибка', 'некорректная открытая экспонента, '
                                'e должно удовлетворять условию 1 < e < φ(n) и быть взаимно простым с φ(n)')

    def encrypt(self):
        try:
            public_key = (self.public_key[0].get(), self.public_key[1].get())
            text = self.text.get('1.0', 'end')[:-1]
            encrypted_text = encode_text(public_key, text)
            self.encrypted_text.delete('1.0', tk.END)
            self.encrypted_text.insert(tk.END, encrypted_text)
        except exceptions.NumberNotNaturalError:
            showerror('Ошибка', 'Все компоненты ключей должны быть натуральными числами')
        except exceptions.InvalidMessage:
            showerror('Ошибка', 'Код символа в тексте должен быть меньше n')

    def decrypt(self):
        try:
            private_key = (self.private_key[0].get(), self.private_key[1].get())
            encrypted_text = self.encrypted_text.get('1.0', 'end')[:-1]
            decrypted_text = encode_text(private_key, encrypted_text)
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, decrypted_text)
        except exceptions.NumberNotNaturalError:
            showerror('Ошибка', 'Все компоненты ключей должны быть натуральными числами')
        except exceptions.InvalidMessage:
            showerror('Ошибка', 'Код символа в тексте должен быть меньше n')

    def generate_e(self):
        try:
            e = generate_e(self.p.get(), self.q.get())
            if e is None:
                showerror('Ошибка', 'Не удалось сгенерировать e')
            else:
                self.e.set(e)
        except exceptions.NumberNotNaturalError:
            showerror('Ошибка', 'p и q должны быть натуральными')
        except exceptions.NumberNotPrimeError:
            showerror('Ошибка', 'p и q должны быть простыми')