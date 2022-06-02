from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread
import tkinter as tk
from .response_window import ResponseWindow
import os


cwd = os.path.abspath(os.path.dirname(__file__))
ICON_PATH = os.path.abspath(os.path.join(cwd, '../files/icon_circle.ico'))


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

    def clear(self):
        self.response_window.scrollable_frame.clear()
        self.response_window.input_frame.clear()

    def write(self, text, font, clear=0):
        """
        :param text: text to be added
        :param font: text font style
        :param clear: 0 - do not clear, 1 - clear before printing, 2 - clear before next printing
        :return: None
        """
        self.response_window.start_progress_bar()
        self.response_window.show_scrollable_frame()
        self.response_window.scrollable_frame.add_text(text, font, clear)

    def get_text_input(self):
        self.response_window.show_input_frame()

    def on_quit(self):
        print('Good bye')
        self.destroy()

    def _prepare_interface(self):
        self.overrideredirect(True)
        self.geometry("300x200-10-50")
        self.attributes("-topmost", True)
