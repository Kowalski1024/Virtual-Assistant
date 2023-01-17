from typing import TYPE_CHECKING

import customtkinter as ctk
import tkinter as tk

from assistant.view.frames import MenuFrame, TextFrame
from assistant.view.key_listener import KeyListener
from assistant.view.popup_window import PopupWindow


if TYPE_CHECKING:
    from assistant.controller import Controller


class GUI(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self._controller: Controller | None = None

        self._key_listener = KeyListener(self.activate).start()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self._menu_frame = MenuFrame(self, fg_color='black', corner_radius=0)
        self._menu_frame.grid(row=0, column=0, sticky="NEW")

        self._text_frame = TextFrame(self)
        self._text_frame.grid(row=1, column=0, sticky="NSEW")

        self._bottom_frame = ctk.CTkLabel(self, fg_color='#111111', corner_radius=0, wraplength=280, text='')
        self._bottom_frame.grid(row=2, column=0, sticky="SEW")

    def prepare_gui(self):
        self.text_frame.clear()
        self.set_bottom_text('')
        self.set_menu_text('Waiting for command')
        self._menu_frame.show_cancel()
        self.show()

    def clear_gui(self):
        self.hide()
        self._menu_frame.hide_cancel()

    def show_reminders(self):
        reminders = self._controller.get_reminders()
        if reminders:
            mess = '\n'.join(f'{date}: {message}' for date, message in reminders)
            self.create_popup(mess)
        self.after(ms=1000, func=self.show_reminders)

    @staticmethod
    def create_popup(message: str):
        PopupWindow(message=message)

    @property
    def text_frame(self):
        return self._text_frame

    @property
    def menu_frame(self):
        return self._menu_frame

    @property
    def bottom_frame(self):
        return self._bottom_frame

    def hide(self):
        self.master.iconify()

    def show(self):
        self.master.deiconify()

    def set_controller(self, controller):
        self._controller = controller

    def set_recognizer(self, choice):
        self._controller.set_recognizer(choice)

    def activate(self):
        self._controller.activate()

    def cancel_pressed(self, state):
        self._controller.cancel(state)



