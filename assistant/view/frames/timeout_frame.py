import customtkinter as ctk
import tkinter as tk


class TimeoutFrame(ctk.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.progressbar = ctk.CTkProgressBar(master=self, determinate_speed=0.1)
        self.progressbar.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
        self.set(0)

    def set(self, value):
        self.progressbar.set(value)

    def get(self):
        return self.progressbar.get()

    def start(self):
        self.progressbar.start()

    def stop(self):
        self.progressbar.stop()
        self.set(100)
