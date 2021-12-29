import tkinter as tk
from rsa.exceptions import *
from rsa.digital_signature import sign_message, verify_signature
from md5 import md5
from sha_1 import sha1
from tkinter.messagebox import showerror, showinfo

class RsaSignatureFrame(tk.Frame):

    HASH_FUNCTIONS = {
        'sha1': 'SHA-1',
        'md5': 'MD5'
    }

    def __init__(self, master):
        super().__init__(master)

        self.message = tk.StringVar()
        self.hash_function = tk.StringVar(value=self.HASH_FUNCTIONS['sha1'])
        self.private_key = (tk.IntVar(), tk.IntVar())
        self.public_key = (tk.IntVar(), tk.IntVar())
        self.signature = tk.IntVar()

        tk.Label(self, text='Цифровая подпись RSA').pack()

        hash_function_frame = tk.Frame(self)
        tk.Label(hash_function_frame, text='Хеш-функция').pack(side='left')
        tk.OptionMenu(hash_function_frame, self.hash_function, *self.HASH_FUNCTIONS.values()).pack(side='left')
        hash_function_frame.pack()

        message_frame = tk.Frame(self)
        tk.Label(message_frame, text='Сообщение =').pack(side='left')
        tk.Entry(message_frame, textvariable=self.message).pack(side='left')
        message_frame.pack()
        sign_frame = tk.Frame(self)
        private_key_frame = tk.LabelFrame(sign_frame, text='Закрытый ключ')
        tk.Label(private_key_frame, text='d =').pack(side='left')
        tk.Entry(private_key_frame, textvariable=self.private_key[0]).pack(side='left')
        tk.Label(private_key_frame, text='n =').pack(side='left')
        tk.Entry(private_key_frame, textvariable=self.private_key[1]).pack(side='left')
        private_key_frame.pack(side='left')
        tk.Button(sign_frame, text='Подписать сообщение', command=self.sign_message).pack(side='left')
        sign_frame.pack()

        signature_frame = tk.Frame(self)
        tk.Label(signature_frame, text='Подпись =').pack(side='left')
        tk.Entry(signature_frame, textvariable=self.signature).pack(side='left')
        signature_frame.pack()

        verify_frame = tk.Frame(self)
        public_key_frame = tk.LabelFrame(verify_frame, text='Открытый ключ')
        tk.Label(public_key_frame, text='e =').pack(side='left')
        tk.Entry(public_key_frame, textvariable=self.public_key[0]).pack(side='left')
        tk.Label(public_key_frame, text='n =').pack(side='left')
        tk.Entry(public_key_frame, textvariable=self.public_key[1]).pack(side='left')
        public_key_frame.pack(side='left')
        tk.Button(verify_frame, text='Проверить подпись', command=self.verify_signature).pack(side='left')
        verify_frame.pack()

    def get_hash_function(self):
        if self.hash_function.get() == self.HASH_FUNCTIONS['sha1']:
            return sha1
        elif self.hash_function.get() == self.HASH_FUNCTIONS['md5']:
            return md5
        else:
            raise RuntimeError('Invalid hash function option')

    def sign_message(self):
        private_key = self.private_key[0].get(), self.private_key[1].get()
        try:
            self.signature.set(sign_message(self.message.get(), private_key, self.get_hash_function()))
        except NumberNotNaturalError:
            showerror('Ошибка', 'Неправильный закрытый ключ')
        except InvalidMessage:
            showerror('Ошибка', 'n закрытого ключа меньше хеш-суммы')

    def verify_signature(self):
        public_key = self.public_key[0].get(), self.public_key[1].get()
        try:
            result = verify_signature(self.message.get(), public_key, self.get_hash_function())
            if result:
                showinfo('Успех', 'Подпись подлинная')
            else:
                showinfo('Неудача', 'Подпись поддельная')
        except NumberNotNaturalError:
            showerror('Ошибка', 'Неправильный открытый ключ')
        except InvalidMessage:
            showerror('Ошибка', 'n открытого ключа меньше хеш-суммы')
