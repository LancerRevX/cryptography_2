import tkinter as tk
from tkinter.messagebox import showerror
from shamirs_secret_sharing import shamir, InvalidVariableError, generate_p, generate_c, generate_d


class ShamirFrame(tk.Frame):
    ERROR_TITLE = 'Ошибка'
    ERROR_MESSAGES = {
        'invalid_order': 'Порядок p должен быть больше либо равен нулю',
        'invalid_p': 'p должно быть простым числом',
        'invalid_ca': 'ca должно быть натуральным числом, взаимно простым с p-1',
        'invalid_cb': 'cb должно быть натуральным числом, взаимно простым с p-1',
        'invalid_da': 'da должно быть натуральным числом, таким, что ca*da mod p-1 == 1',
        'invalid_db': 'db должно быть натуральным числом, таким, что cb*db mod p-1 == 1',
        'invalid_m': 'Сообщение должно быть натуральным числом меньше p'
    }

    def __init__(self, master):
        super().__init__(master)

        self.m = tk.IntVar()
        self.p = tk.IntVar()
        self.p_order = tk.IntVar()
        self.ca = tk.IntVar()
        self.cb = tk.IntVar()
        self.da = tk.IntVar()
        self.db = tk.IntVar()

        self.x1 = tk.IntVar()
        self.x2 = tk.IntVar()
        self.x3 = tk.IntVar()
        self.x4 = tk.IntVar()

        p_frame = tk.Frame(self)
        tk.Label(p_frame, text='p =').grid(row=0, column=0, sticky='e')
        tk.Entry(p_frame, textvariable=self.p).grid(row=0, column=1, sticky='w')
        tk.Label(p_frame, text='Порядок =').grid(row=1, column=0)
        tk.Entry(p_frame, textvariable=self.p_order).grid(row=1, column=1)
        tk.Button(p_frame, text='Генерировать', command=self.generate_p).grid(row=0, column=2, rowspan=2)
        p_frame.grid(row=0, pady=16)

        c_frame = tk.Frame(self)
        tk.Label(c_frame, text='ca =').grid(row=0, column=0)
        tk.Entry(c_frame, textvariable=self.ca).grid(row=0, column=1)
        tk.Label(c_frame, text='cb =').grid(row=0, column=2)
        tk.Entry(c_frame, textvariable=self.cb).grid(row=0, column=3)
        tk.Button(c_frame, text='Генерировать', command=self.generate_c).grid(row=1, column=0, columnspan=4)
        c_frame.grid(row=1, pady=(0, 16))

        d_frame = tk.Frame(self)
        tk.Label(d_frame, text='da =').grid(row=0, column=0)
        tk.Entry(d_frame, textvariable=self.da).grid(row=0, column=1)
        tk.Label(d_frame, text='db =').grid(row=0, column=2)
        tk.Entry(d_frame, textvariable=self.db).grid(row=0, column=3)
        tk.Button(d_frame, text='Генерировать', command=self.generate_d).grid(row=1, column=0, columnspan=4)
        d_frame.grid(row=2, pady=(0, 16))

        m_frame = tk.Frame(self)
        tk.Label(m_frame, text='Сообщение m =').grid(row=0, column=0)
        tk.Entry(m_frame, textvariable=self.m).grid(row=0, column=1)
        m_frame.grid(row=3, pady=(0, 16))

        tk.Button(self, text='Передать сообщение', command=self.send_message).grid(row=4, pady=(0, 16))

        x_frame = tk.Frame(self)
        tk.Label(x_frame, text='x1 =').grid(row=0, column=0)
        tk.Label(x_frame, textvariable=self.x1).grid(row=0, column=1)
        tk.Label(x_frame, text='x2 =').grid(row=1, column=0)
        tk.Label(x_frame, textvariable=self.x2).grid(row=1, column=1)
        tk.Label(x_frame, text='x3 =').grid(row=2, column=0)
        tk.Label(x_frame, textvariable=self.x3).grid(row=2, column=1)
        tk.Label(x_frame, text='x4 =').grid(row=3, column=0)
        tk.Label(x_frame, textvariable=self.x4).grid(row=3, column=1)
        x_frame.grid(row=5, pady=(0, 8))

    def generate_p(self):
        try:
            self.p.set(generate_p(self.p_order.get()))
        except InvalidVariableError as error:
            if error.variable == 'order':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_order'])
            else:
                raise

    def generate_c(self):
        try:
            ca, cb = generate_c(self.ca.get() + 1, self.p.get())
            self.ca.set(ca)
            self.cb.set(cb)
        except InvalidVariableError as error:
            if error.variable == 'p':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_p'])
            else:
                raise

    def generate_d(self):
        try:
            da, db = generate_d(self.ca.get(), self.cb.get(), self.p.get())
            self.da.set(da)
            self.db.set(db)
        except InvalidVariableError as error:
            if error.variable == 'p':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_p'])
            elif error.variable == 'ca':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_ca'])
            elif error.variable == 'cb':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_cb'])

    def send_message(self):
        try:
            x1, x2, x3, x4 = shamir(
                self.m.get(), self.p.get(),
                self.ca.get(), self.da.get(),
                self.cb.get(), self.db.get())
            self.x1.set(x1)
            self.x2.set(x2)
            self.x3.set(x3)
            self.x4.set(x4)
        except InvalidVariableError as error:
            if error.variable == 'm':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_m'])
            elif error.variable == 'p':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_p'])
            elif error.variable == 'ca':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_ca'])
            elif error.variable == 'cb':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_cb'])
            elif error.variable == 'da':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_da'])
            elif error.variable == 'db':
                showerror(self.ERROR_TITLE, self.ERROR_MESSAGES['invalid_db'])
            else:
                raise
