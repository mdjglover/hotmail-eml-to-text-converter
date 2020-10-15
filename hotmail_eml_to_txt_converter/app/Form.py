import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import ttk

class Form(tk.Frame):
    def __init__(self, controller, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller

        source_row = PathSelectFormRow(controller, "Source", 0, master).grid()
        output_row = PathSelectFormRow(controller, "Output", 1, master).grid()
        button = ttk.Button(master, command=controller.convert_eml_to_txt, text="Convert").grid(pady="8")


class PathSelectFormRow(tk.Frame):
    def __init__(self, controller, directory_type, row, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller
        self.directory_type = directory_type
        self.var = tk.StringVar()
        self.var.trace("w", self.set_directory)

        label = ttk.Label(master, text=f"{directory_type} directory: ").grid(row=row, column=0, padx="4")
        entry = ttk.Entry(master, textvariable=self.var, width=50).grid(row=row, column=1)
        button = ttk.Button(master, text="Browse", command=self.select_path).grid(row=row, column=2, padx="4")
    
    def set_directory(self, *args):
        self.controller.set_directory(self.directory_type, self.var.get())
    
    def select_path(self):
        self.var.set(askdirectory())