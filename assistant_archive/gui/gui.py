from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread
import tkinter as tk
import os

from .response_window import ResponseWindow
from .. import FontStyles

cwd = os.path.abspath(os.path.dirname(__file__))
ICON_PATH = os.path.abspath(os.path.join(cwd, '../files/icon_circle.ico'))


class GUI(tk.Tk):
    def __init__(self, pipe):
        super().__init__()
        self.response_window = ResponseWindow(self, pipe)
        self.tray_icon = Icon('Virtual Assistant', Image.open(ICON_PATH), menu=Menu(MenuItem('Quit', self.on_quit)))
        self.thread_tray_icon = Thread(target=self.tray_icon.run, daemon=True)

    def run(self) -> None:
        """
        Run GUI in main thread
        """
        self.thread_tray_icon.start()
        self._prepare_interface()
        self.mainloop()

    def clear(self) -> None:
        """
        Clear text from scrollable frame and input frame
        """
        self.response_window.scrollable_frame.clear()
        self.response_window.input_frame.clear()

    def write(self, text: str, font: FontStyles, clear: int = 0) -> None:
        """
        Writes text to scrolling frame, starting a timer after which the window will be hidden. Timer can be stopped by
        clicking on title bar
        :param text: text to be added
        :param font: text font style
        :param clear: 0 - do not clear, 1 - clear before printing, 2 - clear before next printing
        :return: None
        """
        self.response_window.start_progress_bar()
        self.response_window.show_scrollable_frame()
        self.response_window.scrollable_frame.add_text(text, font, clear)

    def get_text_input(self) -> None:
        """
        Shows the input frame
        """
        self.response_window.show_input_frame()

    def on_quit(self) -> None:
        """
        Destroy GUI when user want to quit from assistant_archive
        """
        print('Good bye')
        self.destroy()

    def _prepare_interface(self) -> None:
        # Prepare tkinter GUI
        self.overrideredirect(True)
        self.geometry("300x200-10-50")
        self.attributes("-topmost", True)
