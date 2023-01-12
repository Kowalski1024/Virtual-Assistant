import customtkinter as ctk
import tkinter as tk


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.combobox = ctk.CTkComboBox(
            master=self,
            values=["Whisper", "GoogleAPI"],
            fg_color='#222222',
            button_color='#222222'
        )
        self.combobox.grid(row=0, column=0, sticky="NE")

        self.label = ctk.CTkLabel(self, text="Welcome!", fg_color='#111111', wraplength=280)
        self.label.grid(row=1, column=0, sticky="WE")

    def set_text(self, text: str):
        self.label.configure(text=text)

