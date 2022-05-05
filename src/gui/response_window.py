import tkinter as tk


class ResponseWindow(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        raise NotImplementedError

    def switch_type(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def _on_resize(self, event):
        raise NotImplementedError

    def _return_x_on_hovering(self, event):
        raise NotImplementedError

    def _prepare(self, event):
        raise NotImplementedError
