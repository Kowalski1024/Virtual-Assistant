import customtkinter as ctk
import tkinter as tk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')
        self.geometry("400x240")

        button = ctk.CTkButton(master=self, text="CTkButton", command=button_function)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def button_function():
    print("button pressed")


if __name__ == '__main__':
    app = App()
    app.mainloop()