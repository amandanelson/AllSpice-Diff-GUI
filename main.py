""" GUI for AllSpice https://www.allspice.io/diff-tool """

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as ms
import os
import subprocess
import webbrowser
from PIL import Image, ImageTk


class HomePage:
    def __init__(self, root: ttk):
        root.title("AllSpice Diff Comparison Tool")
        root.iconphoto(False, PhotoImage(file='allspiceicon.png'))
        root.geometry("600x180")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # frame creation
        homepage = ttk.Frame(root, padding="3 3 12 12")
        homepage.grid(column=0, row=0, columnspan=2, rowspan=2, sticky="NWES")
        homepage.columnconfigure(1, weight=1)
        homepage.columnconfigure(2, weight=1)
        homepage.rowconfigure(1, weight=1)
        homepage.rowconfigure(2, weight=1)
        homepage.rowconfigure(3, weight=1)

        self.home = os.path.join(os.path.expanduser('~'), 'Documents')
        self.file_types = (
            ('PCB Files', '*.schdoc *.SchDoc *.pcbdoc *.PcbDoc *.csv *.CSV'),
            ('All files', '*.*'))

        if os.path.isdir("D:\\SVN\\Engineering\\ECAD\\PRJ129\\PRJ129-2053-00"):
            self.initial_dir = "D:\\SVN\\Engineering\\ECAD\\PRJ129\\PRJ129-2053-00"
        else:
            self.initial_dir = os.path.expanduser('~')

        # menu
        menubar = Menu(root)
        file_menu = Menu(menubar, tearoff=0)
        root['menu'] = menubar
        file_menu.add_command(label='Clear Files', command=self.clear_files)
        file_menu.add_command(label='AllSpice Diff Website',
                              command=lambda url='https://www.allspice.io/diff-tool':
                              webbrowser.open_new_tab(url))
        file_menu.add_command(label='Github Website',
                              command=lambda url='https://github.com/amandanelson/AllSpice-Diff-GUI':
                              webbrowser.open_new_tab(url))
        menubar.add_cascade(menu=file_menu, label='Tools')

        # row 1: file 1 button + label
        self.file_one = ""
        self.file_one_response = StringVar(value='Select a file')
        self.file_one_label = ttk.Entry(homepage, background='white', foreground='gray', width=80,
                                   textvariable=self.file_one_response)
        self.file_one_label.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)
        file_one_button = ttk.Button(homepage, text="New File", command=self.load_file_one)
        file_one_button.grid(row=1, column=3, sticky='w', padx=10)

        # row 2: file 2 button + label
        self.file_two = ""
        self.file_two_response = StringVar(value='Select a file')
        self.file_two_label = ttk.Entry(homepage, background='white', foreground='gray', width=80,
                                   textvariable=self.file_two_response)
        self.file_two_label.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)
        self.file_two_button = ttk.Button(homepage, text="Old File", command=self.load_file_two)
        self.file_two_button.grid(row=2, column=3, sticky='w', padx=10)
        self.file_two_button['state'] = DISABLED

        # row 3: compare button
        image = Image.open('allspiceicon.png')
        image = image.resize((40, 40), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.compare_button = ttk.Button(homepage, image=self.img, text="Show Diff", compound=LEFT, command=self.compare)
        self.compare_button.grid(column=1, row=3, columnspan=3)
        self.compare_button['state'] = DISABLED

    def load_file_one(self):
        filename = fd.askopenfilename(title='Select a file', initialdir=self.initial_dir,
                                      filetypes=self.file_types)
        if filename:
            self.file_one = filename
            self.file_one_response.set(filename)
        if self.file_one != '':
            self.file_one_label.configure(foreground='black')
            self.file_two_button['state'] = NORMAL
            self.compare_button['state'] = NORMAL

    def load_file_two(self):
        filename = fd.askopenfilename(title='Select a file', initialdir=os.path.dirname(self.file_one),
                                      filetypes=self.file_types)
        if filename:
            self.file_two_label.configure(foreground='black')
            self.file_two = filename
            self.file_two_response.set(filename)

    def compare(self):
        try:
            if self.file_two != '':
                subprocess.run(['AllSpice', '--show', self.file_one, '--diff', self.file_two], shell=True, check=True)
            else:
                subprocess.run(['AllSpice', '--show', self.file_one], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            ms.showerror("AllSpice Diff Not Found",
                         "Please make sure AllSpice Diff is installed and added to your PATH.")

    def clear_files(self):
        self.file_one = ''
        self.file_one_response.set("File cleared")
        self.file_one_label.configure(foreground='gray')
        self.file_two = ''
        self.file_two_response.set("File cleared")
        self.file_two_label.configure(foreground='gray')
        self.file_two_button['state'] = DISABLED
        self.compare_button['state'] = DISABLED


if __name__ == '__main__':
    root = Tk()
    HomePage(root)
    root.mainloop()
