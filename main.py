""" GUI for AllSpice https://www.allspice.io/diff-tool """

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
import subprocess


class HomePage:
    def __init__(self, root: ttk):
        root.title("AllSpice Comparison Tool")

        # frame creation
        homepage = ttk.Frame(root, padding="3 3 12 12")
        homepage.grid(column=2, row=2, sticky=(N, W, E, S))
        homepage.columnconfigure(0, weight=1)
        homepage.columnconfigure(1, weight=1)
        homepage.rowconfigure(0, weight=1)
        homepage.rowconfigure(1, weight=1)

        self.home = os.path.join(os.path.expanduser('~'), 'Documents')
        self.file_types = (
            ('Schematics', '*.schdoc'),
            ('PCBs', '*.pcbdoc'),
            ('CSVs', '*.csv'),
            ('All files', '*.*'))

        self.initial_dir = "Y:\\Released\\028-PCB (Printed Circuit Board)\\PCB028-0258-01"
        # TODO: fix initial_dir

        # row 0: load file 1 button + label
        self.file_one = ""
        self.file_one_response = StringVar()
        file_one_button = ttk.Button(homepage, text="Select File 1", command=self.load_file_one)
        file_one_button.grid(column=0, row=0, sticky='nw', padx=10, pady=10)
        ttk.Label(homepage, textvariable=self.file_one_response).grid(column=2, row=0, sticky='w')

        # row 1
        self.file_two = ""
        self.file_two_response = StringVar()
        file_two_button = ttk.Button(homepage, text="Select File 2", command=self.load_file_two)
        # TODO: add disable file_two_button till file_one is not ""
        file_two_button.grid(column=0, row=1, sticky='nw', padx=10, pady=10)
        ttk.Label(homepage, textvariable=self.file_two_response).grid(column=2, row=1, sticky='w')

        # row 2
        compare_button = ttk.Button(homepage, text="Compare!", command=self.compare)
        # TODO: add disable compare till file_one and file_two are not ""
        compare_button.grid(column=0, row=2)

        # row 3
        # TODO: add reference to AllSpice
        # TODO: fix layout

    def load_file_one(self):
        filename = fd.askopenfilename(title='Select a file', initialdir=self.initial_dir,)
        if filename:
            self.file_one = filename
            self.file_one_response.set(f"Selected {filename}")

    def load_file_two(self):
        filename = fd.askopenfilename(title='Select a file', initialdir=os.path.dirname(self.file_one),)
        if filename:
            self.file_two = filename
            self.file_two_response.set(f"Selected {filename}")

    def compare(self):
        allspice = os.path.join(os.path.expanduser('~'), 'AppData\\Local\\Programs\\allspice\\AllSpice.exe')
        # TODO: make this path not brittle?
        subprocess.call([allspice, '--show', self.file_one, '--diff', self.file_two])


if __name__ == '__main__':
    root = Tk()
    HomePage(root)
    root.mainloop()
