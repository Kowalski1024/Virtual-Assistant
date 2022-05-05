import tkinter as tk


class InputFrame(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        raise NotImplementedError

    def _send(self):
        raise NotImplementedError

    def _prepare_frame(self):
        raise NotImplementedError
