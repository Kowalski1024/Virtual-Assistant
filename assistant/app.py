import customtkinter as ctk
import tkinter as tk

from assistant.view import GUI
from assistant.controller import Controller


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        w = 300  # width for the Tk root
        h = 400  # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws - ws / 12) - (w / 2)
        y = (hs - hs / 5) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title('Virtual Assistant')
        self.attributes("-topmost", True)
        self.minsize(width=280, height=300)

        view = GUI(self)
        view.pack(fill=tk.BOTH, expand=1)

        controller = Controller(view=view, model=None)
        view.set_controller(controller)

        self.bind('<Control-q>', self.activate)

    def activate(self, event):
        print('XD')


if __name__ == '__main__':
    app = App()
    app.mainloop()
