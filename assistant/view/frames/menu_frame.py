import customtkinter as ctk
import tkinter as tk


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.combobox = ctk.CTkComboBox(
            master=self,
            values=["GoogleAPI", "Whisper"],
            command=master.set_recognizer,
            fg_color='#222222',
            button_color='#222222'
        )
        self.combobox.grid(row=0, column=2, sticky="NE")

        self._cancel_var = tk.BooleanVar(self)
        self.check_box = ctk.CTkCheckBox(
            master=self,
            text="Cancel",
            command=self._cancel,
            variable=self._cancel_var,
            onvalue=True, offvalue=False
        )

        self.label = ctk.CTkLabel(self, text="Welcome!", fg_color='#111111', wraplength=280)
        self.label.grid(row=1, column=0, columnspan=3, sticky="WE")

    def set_info_bar(self, text: str):
        self.label.configure(text=text)

    def show_cancel(self):
        self.check_box.deselect()
        self.check_box.grid(row=0, column=1, sticky="NW")

    def hide_cancel(self):
        self.check_box.grid_remove()

    def _cancel(self):
        self.master.cancel_pressed(self._cancel_var.get())
