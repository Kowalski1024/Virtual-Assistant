import time
from threading import Thread
import tkinter as tk
from tkinter import ttk

from .input_frame import InputFrame
from .scrollable_text_frame import ScrollableTextFrame
from . import colors
from .. import Response, ResponseType


class ResponseWindow(tk.Frame):
    def __init__(self, parent: tk.Tk, pipe):
        super().__init__(parent, bg=colors.RGRAY)
        self._pipe = pipe
        self._progress_bar_thread = Thread()
        self._progress_stop_flag = False

        # styles
        self.container = tk.Frame(self, bg=colors.DGRAY, highlightthickness=0, padx=4, pady=4)
        self.input_frame = InputFrame(self._send_input_text, self.container, bg=colors.DGRAY, highlightthickness=0)
        self.scrollable_frame = ScrollableTextFrame(self.container, bg=colors.DGRAY, highlightthickness=0)

        self.title_bar = tk.Frame(self, bg=colors.RGRAY, relief='raised', bd=0, highlightthickness=0)
        self.title_bar_title = tk.Label(self.title_bar, text='', bg=colors.RGRAY, bd=0, fg='white',
                                        font=("helvetica", 10),
                                        highlightthickness=0)
        self.progress_bar = tk.ttk.Progressbar(self, orient=tk.HORIZONTAL, length=260, mode='determinate')

        self.close_button = tk.Button(self.title_bar, text='  ×  ', command=self.hide, bg=colors.RGRAY, padx=2,
                                      pady=2,
                                      font=("calibri", 13), bd=0, fg='white', highlightthickness=0)

        # pack widgets
        self._prepare()

    def show_input_frame(self):
        self.stop_progress_bar()
        self.input_frame.tkraise()
        self.show()

    def show_scrollable_frame(self):
        self.scrollable_frame.tkraise()
        self.show()

    def _send_input_text(self, txt):
        self._pipe.send(Response(ResponseType.TEXT_RESPONSE, txt))
        self.hide()

    def _step_progress_bar(self):
        self.progress_bar['value'] = 0
        while self.progress_bar['value'] != 100:
            self.progress_bar['value'] += 10
            self.update_idletasks()
            time.sleep(1)
            if self._progress_stop_flag:
                self._progress_stop_flag = False
                return
        self.hide()

    def start_progress_bar(self):
        if self._progress_bar_thread.is_alive():
            self.progress_bar['value'] = 0
        else:
            self._progress_bar_thread = Thread(target=self._step_progress_bar, daemon=True)
            self._progress_bar_thread.start()

    def stop_progress_bar(self):
        if self._progress_bar_thread.is_alive():
            self._progress_stop_flag = True

    def hide(self):
        self.master.withdraw()
        self.input_frame.clear()
        self.scrollable_frame.clear()

    def show(self):
        self.master.deiconify()

    def _change_x_on_hovering(self, event):
        self.close_button['bg'] = 'red'

    def _return_x_to_normal_state(self, event):
        self.close_button['bg'] = colors.RGRAY

    def _get_pos(self, event):
        def move_window(event):
            self.config(cursor="fleur")
            self.master.geometry(f'+{event.x_root + x_win}+{event.y_root + y_win}')

        def release_window(event):
            self.config(cursor="arrow")

        self.stop_progress_bar()

        x_win = self.master.winfo_x()
        y_win = self.master.winfo_y()

        start_x = event.x_root
        start_y = event.y_root

        y_win = y_win - start_y
        x_win = x_win - start_x

        self.title_bar.bind('<B1-Motion>', move_window)
        self.title_bar.bind('<ButtonRelease-1>', release_window)
        self.title_bar_title.bind('<B1-Motion>', move_window)
        self.title_bar_title.bind('<ButtonRelease-1>', release_window)

    def _prepare(self):
        self.title_bar.pack(fill=tk.X)
        self.close_button.pack(side=tk.RIGHT, ipadx=7, ipady=1)
        self.title_bar_title.pack(side=tk.LEFT, padx=10)
        self.progress_bar.pack(side=tk.BOTTOM)
        self.container.pack(expand=1, fill=tk.BOTH, ipadx=1, ipady=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.title_bar.bind('<Button-1>', self._get_pos)
        self.title_bar_title.bind('<Button-1>', self._get_pos)
        self.close_button.bind('<Enter>', self._change_x_on_hovering)
        self.close_button.bind('<Leave>', self._return_x_to_normal_state)
        self.pack(side="top", fill="both", expand=True)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.input_frame.grid(row=0, column=0, sticky="nsew")
        self.hide()
