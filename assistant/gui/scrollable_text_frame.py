import tkinter as tk

from .. import FontStyles


class ScrollableTextFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.txt = tk.Text(self, wrap=tk.WORD)
        self.txt.grid(row=0, column=0, sticky=tk.NSEW, padx=2, pady=2)
        # self.txt.config(state=tk.DISABLED)
        scrollb = tk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky=tk.NSEW)
        self.txt['yscrollcommand'] = scrollb.set
        self._clear_flag = False
        self._prepare_fonts()

    def clear(self):
        self.txt.delete(1.0, tk.END)

    def add_text(self, text: str, font: FontStyles, clear):
        if clear == 1 or self._clear_flag:
            self.clear()
            self._clear_flag = False
        elif clear == 2:
            self._clear_flag = clear
        self.txt.insert(tk.END, text+"\n", font)

    def _prepare_fonts(self):
        for font in FontStyles:
            self.txt.tag_configure(font, font=font.value)
