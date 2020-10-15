from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from hotmail_eml_to_txt_converter.app.Form import Form
from hotmail_eml_to_txt_converter.parser.HotmailEMLChainParser import HotmailEMLChainParser

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().wm_title("Hotmail .eml to .txt Converter")

        container = tk.Frame(self)
        container.grid(padx=8, pady=16)

        controller = AppController()

        form = Form(controller, container).grid()
        

class AppController():
    def __init__(self):
        self.source_directory_path = ""
        self.output_directory_path = ""

    def convert_eml_to_txt(self):
        # Goes through each .eml file in input_directory and outputs
        # them as .txt files in output_directory
        if self.source_directory_path == "" or self.output_directory_path == "":
            messagebox.showerror("Error", "Source and output directories must be specified.")
            return

        # Get all full file paths of .eml files    
        files = [self.source_directory_path + "/" + f for f in listdir(self.source_directory_path) if isfile(join(self.source_directory_path, f)) and f.endswith(".eml")]

        if len(files) == 0:
            messagebox.showerror("Error", f"No .eml files were found in {self.source_directory_path}")
            return
            
        total_emails = 0

        for f in files:
            emails = []
            with open(f) as eml:
                parser = HotmailEMLChainParser(eml)
                emails = parser.get_emails()
                        
            for email in emails:
                output_filename = f"{email.date} {email.time} - {email.sender_email}"
                output_path = f"{self.output_directory_path}/{output_filename}.txt".replace("/", "\\")
                with open(output_path, mode="w") as output_file:
                    output_file.write(str(email))

                total_emails += 1
        
        completion_text =  f"{len(files)} .eml files were found in {self.source_directory_path}\n"
        completion_text += "\n"
        completion_text += f"{total_emails} .txt files have been output to {self.output_directory_path}"

        messagebox.showinfo("Complete", completion_text)
    

    def set_directory(self, directory_type, path):
        if directory_type == "Source":
            self.source_directory_path = path
        elif directory_type == "Output":
            self.output_directory_path = path