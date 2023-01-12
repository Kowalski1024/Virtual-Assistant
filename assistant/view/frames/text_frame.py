import customtkinter as ctk
import tkinter as tk


class TextFrame(ctk.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)