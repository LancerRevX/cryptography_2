import tkinter as tk
from gcd_frame import GcdFrame
from inversion_frame import InversionFrame
from mod_exp_frame import ModExpFrame


class CryptographyInterface(tk.Tk):
    PADDING = 32

    def __init__(self):
        super().__init__()

        self.title('Криптография')

        self.back_button = tk.Button(
            self,
            text='Назад',
            command=lambda: self.switch_to_frame(self.main_frame)
        )
        self.gcd_frame = GcdFrame(self)
        self.inversion_frame = InversionFrame(self)
        self.mod_exp_frame = ModExpFrame(self)

        self.main_frame = tk.Frame()
        tk.Button(
            self.main_frame,
            text='Наибольший общий делитель',
            command=lambda: self.switch_to_frame(self.gcd_frame)
        ).pack()
        tk.Button(
            self.main_frame,
            text='Инверсия по модулю',
            command=lambda: self.switch_to_frame(self.inversion_frame)
        ).pack()
        tk.Button(
            self.main_frame,
            text='Возведение в степень по модулю',
            command=lambda: self.switch_to_frame(self.mod_exp_frame)
        ).pack()

        self.current_frame = self.main_frame
        self.switch_to_frame(self.main_frame)

        self.resizable(False, False)
        self.wm_attributes('-toolwindow', 'True')

    def switch_to_frame(self, frame):
        self.current_frame.grid_remove()
        if frame is self.main_frame:
            self.back_button.grid_remove()
            frame.grid(row=0, column=0, padx=self.PADDING)
        else:
            self.back_button.grid(row=0, column=0)
            frame.grid(row=1, column=0, padx=self.PADDING)
        self.current_frame = frame


if __name__ == '__main__':
    CryptographyInterface().mainloop()
