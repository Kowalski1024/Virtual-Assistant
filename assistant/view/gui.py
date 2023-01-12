from threading import Thread

import customtkinter as ctk
import tkinter as tk

from .frames import MenuFrame, TimeoutFrame, TextFrame


class GUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self._menu_frame = MenuFrame(self, fg_color='black', corner_radius=0)
        self._menu_frame.grid(row=0, column=0, sticky="NEW")

        self._container = TextFrame(self)
        self._container.grid(row=1, column=0, sticky="NSEW")

        self._timeout_frame = TimeoutFrame(self, fg_color='black', corner_radius=0)
        self._timeout_frame.grid(row=2, column=0, sticky="SEW")

    @staticmethod
    def input_dialog(text: str, title: str):
        dialog = ctk.CTkInputDialog(text=text, title=title)
        return dialog.get_input()

    def text_box(self) -> TextFrame:
        return self._container

    def hide(self):
        self.master.iconify()

    def show(self):
        self.master.deiconify()


