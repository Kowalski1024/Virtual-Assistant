from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread
import tkinter as tk
from .response_window import ResponseWindow


ICON_PATH = "src/files/icon_circle.ico"


class GUI(tk.Tk):
    def __init__(self, pipe):
        super().__init__()
        self.response_window = ResponseWindow(self, pipe)
        self.tray_icon = Icon('Virtual Assistant', Image.open(ICON_PATH), menu=Menu(MenuItem('Quit', self.on_quit)))
        self.thread_tray_icon = Thread(target=self.tray_icon.run, daemon=True)

    def run(self):
        self.thread_tray_icon.start()
        self._prepare_interface()
        self.mainloop()

    def on_quit(self):
        print('Good bye')
        self.root.destroy()

    def _prepare_interface(self):
        self.overrideredirect(True)
        self.geometry("300x200-10-50")
        self.attributes("-topmost", True)
