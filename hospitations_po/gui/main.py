from http import server
import tkinter as tk
import tkinter.ttk as ttk
import os
from typing import Optional
from frames import LoginFrame


class MainWindow(tk.Tk):
    frame: Optional[tk.Frame] = None
    user_id: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.title('Twoje Hospitacje')

        self.tk.call(
            'source',
            os.path.join(os.getcwd(),
                         'hospitations_po/gui/azure dark/azure dark.tcl'))
        ttk.Style(self).theme_use('azure')

        self.geometry('1200x750+0+0')
        self.resizable(False, False)

        self.iconbitmap(
            os.path.join(os.getcwd(),
                         'hospitations_po/gui/icons/main_icon.ico'))
        self.frame: tk.Frame = LoginFrame(self)
        self.frame.pack(fill="both", expand=True)


if __name__ == '__main__':
    main_window: MainWindow = MainWindow()
    main_window.mainloop()
