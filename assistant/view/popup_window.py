import customtkinter as ctk
import tkinter as tk


class PopupWindow(ctk.CTkToplevel):
    def __init__(self, *args, message: str, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("280x100")
        self.title('Reminders')

        label = ctk.CTkLabel(self, text=message)
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
