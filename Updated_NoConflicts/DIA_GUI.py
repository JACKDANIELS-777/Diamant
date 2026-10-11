import tkinter as tk

class DiaGUI:
    def __init__(self):
        self.root = None

    def Window(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        return self.root

    def Label(self, parent, text):
        lbl = tk.Label(parent, text=text)
        lbl.pack()
        return lbl

    def Button(self, parent, text):
        btn = tk.Button(parent, text=text)
        btn.pack()
        return btn

    def show(self, window):
        window.mainloop()
