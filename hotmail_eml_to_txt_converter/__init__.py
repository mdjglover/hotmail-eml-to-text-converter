import sys
import os
import tkinter as tk
from tkinter import ttk

from hotmail_eml_to_txt_converter.app.App import App

def run_app():
    app = App()
    app.mainloop()