import os
import tempfile
import tkinter as tk
import webbrowser
from tkinter import filedialog, simpledialog

import markdown

from merg import merge_pdfs
from pdf import ontop, sbs
from title import create_titles_pdf


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Label to guide user
        self.instruction = tk.Label(
            self, text="Select Horizontal or Vertical Comparison:"
        )
        self.instruction.pack(side="top")

        # Buttons for selection
        self.horizontal_button = tk.Button(
            self, text="Horizontal", command=self.ask_dir_count
        )
        self.horizontal_button.pack(side="left")

        self.vertical_button = tk.Button(self, text="Vertical", command=self.vertical)
        self.vertical_button.pack(side="right")

        # Quit button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def ask_dir_count(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Ask user for number of directories
        self.dir_count = simpledialog.askinteger(
            "Input", "How many directories?", minvalue=1, maxvalue=10
        )
        self.horizontal()

    def horizontal(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.dir_entries = []
        for i in range(self.dir_count):
            entry = self.create_file_input(f"Input Directory {i+1}: ")
            self.dir_entries.append(entry)

        # Output directory
        self.output_dir = self.create_file_input("Output Directory: ")

        # Target size
        self.target_size = self.create_entry("Target Size (width,height): ")

        # Titles option
        self.title_entry = self.create_entry("Enter titles (comma-separated): ")

        # File name
        self.file_name = self.create_entry("Enter file name for saving: ")

        # Submit button
        self.submit = tk.Button(self, text="Create PDF", command=self.run_sbs)
        self.submit.pack()

        # Return to main menu
        self.return_button = tk.Button(
            self, text="Return to main menu", command=self.create_widgets
        )
        self.return_button.pack()

    def vertical(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Input directory
        self.input_dir = self.create_file_input("Input Directory: ")

        # Output directory
        self.output_dir = self.create_file_input("Output Directory: ")

        # Images per page
        self.images_per_page = self.create_entry("Images per page: ")

        # Target size
        self.target_size = self.create_entry("Target Size (width,height): ")

        # Titles option
        self.title_entry = self.create_entry("Enter titles (comma-separated): ")

        # File name
        self.file_name = self.create_entry("Enter file name for saving: ")

        # Submit button
        self.submit = tk.Button(self, text="Create PDF", command=self.run_ontop)
        self.submit.pack()

        # Return to main menu
        self.return_button = tk.Button(
            self, text="Return to main menu", command=self.create_widgets
        )
        self.return_button.pack()

    def create_file_input(self, label_text):
        frame = tk.Frame(self)
        label = tk.Label(frame, text=label_text)
        label.pack(side="left")
        entry = tk.Entry(frame)
        entry.pack(side="left")
        button = tk.Button(
            frame, text="Browse", command=lambda: self.browse_directory(entry)
        )
        button.pack(side="right")
        frame.pack()
        return entry

    def create_entry(self, label_text):
        frame = tk.Frame(self)
        label = tk.Label(frame, text=label_text)
        label.pack(side="left")
        entry = tk.Entry(frame)
        entry.pack(side="right")
        frame.pack()
        return entry

    def browse_directory(self, entry):
        directory = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, directory)

    def run_sbs(self):
        dirs = [entry.get() for entry in self.dir_entries]
        output_pdf = self.output_dir.get() + "/" + self.file_name.get() + ".pdf"
        target_size = eval(self.target_size.get()) if self.target_size.get() else None
        titles = self.title_entry.get().split(",") if self.title_entry.get() else []
        # Pass dirs as a list of directories
        sbs(dirs, output_pdf, target_size)

    def run_ontop(self):
        input_path = self.input_dir.get()
        output_path = self.output_dir.get() + "/" + self.file_name.get() + ".pdf"
        images_per_page = int(self.images_per_page.get())
        target_size = eval(self.target_size.get()) if self.target_size.get() else None
        titles = self.title_entry.get().split(",") if self.title_entry.get() else []
        ontop(input_path, output_path, images_per_page, target_size)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
