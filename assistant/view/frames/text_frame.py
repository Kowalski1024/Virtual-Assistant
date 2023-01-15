from typing import MutableMapping

import customtkinter as ctk
import tkinter as tk


class TextFrame(ctk.CTkTextbox):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

    def clear(self):
        self.delete(1.0, tk.END)

    def set(self, text):
        self.clear()
        self.insert(1.0, text=text)

    def update_observer(self, data):
        text = 'Unknown'

        if isinstance(data, MutableMapping):
            text = '\n'.join(f'{key}: {value}' for key, value in data.items())

        self.set(text)


