from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread
import tkinter as tk
from .response_window import ResponseWindow


ICON_PATH = "src/files/icon_circle.ico"


class GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.response_window = ResponseWindow(self.root)
        self.tray_icon = Icon('Virtual Assistant', Image.open(ICON_PATH), menu=Menu(MenuItem('Quit', self.on_quit)))
        self.thread_tray_icon = Thread(target=self.tray_icon.run, daemon=True)

    def run(self):
        self.thread_tray_icon.start()
        self._prepare_interface()
        self.root.mainloop()

    def on_quit(self):
        print('Good bye')
        self.root.destroy()

    def _prepare_interface(self):
        self.root.overrideredirect(True)
        self.root.geometry("300x200-10-50")
        self.root.attributes("-topmost", True)
