import tkinter as tk

from .input_frame import InputFrame
from .scrollable_text_frame import ScrollableTextFrame
from . import colors


class ResponseWindow(tk.Frame):
    def __init__(self, parent: tk.Tk, pipe):
        super().__init__(parent)
        self.container = tk.Frame(self, bg=colors.DGRAY, highlightthickness=0)
        self.input_frame = InputFrame(pipe, self.container, bg=colors.DGRAY, highlightthickness=0)
        self.scrollable_frame = ScrollableTextFrame(self.container, bg=colors.DGRAY, highlightthickness=0)
        self.title_bar = tk.Frame(self, bg=colors.RGRAY, relief='raised', bd=0, highlightthickness=0)
        self.title_bar_title = tk.Label(self.title_bar, text='', bg=colors.RGRAY, bd=0, fg='white',
                                        font=("helvetica", 10),
                                        highlightthickness=0)
        self.close_button = tk.Button(self.title_bar, text='  ×  ', command=self.hide, bg=colors.RGRAY, padx=2,
                                      pady=2,
                                      font=("calibri", 13), bd=0, fg='white', highlightthickness=0)
        self.resize_x_widget = tk.Frame(self.master, bg=colors.DGRAY, cursor='sb_h_double_arrow')
        self.resize_y_widget = tk.Frame(self.master, bg=colors.DGRAY, cursor='sb_v_double_arrow')
        self._prepare()

    def show_input_frame(self):
        self.input_frame.tkraise()
        self.show()

    def show_scrollable_frame(self):
        self.scrollable_frame.tkraise()
        self.show()

    def hide(self):
        self.master.withdraw()

    def show(self):
        self.master.deiconify()

    def _on_resize(self, event):
        raise NotImplementedError

    def _change_x_on_hovering(self, event):
        self.close_button['bg'] = 'red'

    def _return_x_to_normal_state(self, event):
        self.close_button['bg'] = colors.RGRAY

    def _prepare(self):
        self.title_bar.pack(fill=tk.X)
        self.close_button.pack(side=tk.RIGHT, ipadx=7, ipady=1)
        self.title_bar_title.pack(side=tk.LEFT, padx=10)
        self.resize_x_widget.pack(side=tk.RIGHT, ipadx=2, fill=tk.Y)
        self.resize_y_widget.pack(side=tk.BOTTOM, ipadx=2, fill=tk.X)
        self.container.pack(expand=1, fill=tk.BOTH)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.close_button.bind('<Enter>', self._change_x_on_hovering)
        self.close_button.bind('<Leave>', self._return_x_to_normal_state)
        self.pack(side="top", fill="both", expand=True)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.input_frame.grid(row=0, column=0, sticky="nsew")
