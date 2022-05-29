import tkinter as tk

from .. import Response, ResponseType


class InputFrame(tk.Frame):
    def __init__(self, pipe, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._pipe = pipe
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text='Send', command=lambda: self._send(self.entry.get()))
        self._prepare_frame()

    def _send(self, txt):
        self._pipe.send(Response(ResponseType.TEXT_RESPONSE, txt))

    def _prepare_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.entry.grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)
        self.button.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
