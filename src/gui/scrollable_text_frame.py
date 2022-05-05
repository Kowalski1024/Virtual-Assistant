import tkinter as tk


class ScrollableTextFrame(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        raise NotImplementedError

    def clear_text(self):
        raise NotImplementedError

    def add_text(self, text, font):
        raise NotImplementedError

    def _prepare_fonts(self):
        raise NotImplementedError
