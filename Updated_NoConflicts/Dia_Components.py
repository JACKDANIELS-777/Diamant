import tkinter as tk

class DiaWindow:
    def __init__(self, title, width, height):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.widgets = []

    def add(self, widget):
        self.widgets.append(widget)
        widget.render(self.root)

    def run(self):
        self.root.mainloop()

class DiaLabel:
    def __init__(self, text):
        self.text = text
        self.tk_label = None

    def render(self, parent):
        self.tk_label = tk.Label(parent, text=self.text)
        self.tk_label.pack()

class DiaButton:
    def __init__(self, text, on_click=None):
        self.text = text
        self.on_click = on_click
        self.tk_button = None

    def render(self, parent):
        def callback():
            if self.on_click:
                self.on_click()  # Calls Dia trigger function
        self.tk_button = tk.Button(parent, text=self.text, command=callback)
        self.tk_button.pack()

class DiaEventSystem:
    def __init__(self):
        self.subscribers = {}

    def on(self, event_name, callback):
        self.subscribers[event_name] = callback

    def trigger(self, event_name):
        if event_name in self.subscribers:
            self.subscribers[event_name]()
