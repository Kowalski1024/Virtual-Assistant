import tkinter as tk


class InputFrame(tk.Frame):
    def __init__(self, func, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._func = func
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text='Send', command=lambda: self._func(self.entry.get()))
        self._prepare_frame()

    def clear(self):
        """
        Clear entry widget
        """
        self.entry.delete(0, tk.END)

    def _prepare_frame(self):
        # Prepare frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.entry.grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)
        self.button.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
