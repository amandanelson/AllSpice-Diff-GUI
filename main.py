""" GUI for AllSpice https://www.allspice.io/diff-tool """

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from os import path
import subprocess
import webbrowser
from PIL import Image, ImageTk


class HomePage:
    def __init__(self, window: ttk):
        # window properties
        window.title("AllSpice Diff Comparison Tool")
        path_to_image = path.abspath(path.join(path.dirname(__file__), 'allspice-icon.png'))
        window.iconphoto(False, PhotoImage(file=path_to_image))
        window.geometry("600x180")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        # frame creation
        homepage = ttk.Frame(window, padding="3 3 12 12")
        homepage.grid(column=0, row=0, columnspan=2, rowspan=2, sticky="NEWS")
        homepage.columnconfigure(1, weight=1)
        homepage.columnconfigure(2, weight=1)
        homepage.rowconfigure(1, weight=1)
        homepage.rowconfigure(2, weight=1)
        homepage.rowconfigure(3, weight=1)

        # menu
        menu_bar = Menu(window)
        self.tool_menu = Menu(menu_bar, tearoff=0)
        help_menu = Menu(menu_bar, tearoff=0)
        window['menu'] = menu_bar
        menu_bar.add_cascade(menu=self.tool_menu, label='Tools')
        menu_bar.add_cascade(menu=help_menu, label='Help')
        self.tool_menu.add_command(label='Clear Files', command=self.clear_files)
        self.tool_menu.entryconfigure(1, state=DISABLED)
        help_menu.add_command(label='AllSpice Diff Website',
                              command=lambda url='https://www.allspice.io/diff-tool':
                              webbrowser.open_new_tab(url))
        # help_menu.add_command(label='About',
        #                      command=lambda url='https://github.com/amandanelson/AllSpice-Diff-GUI':
        #                      webbrowser.open_new_tab(url))

        # LAYOUT
        # row 1: file 1 button + label
        self.file_one = StringVar(value='Select a file')
        self.file_one_entry = ttk.Entry(homepage, width=80, textvariable=self.file_one, state=DISABLED)
        self.file_one_entry.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)
        file_one_button = ttk.Button(homepage, text="New File", command=self.load_file_one)
        file_one_button.grid(row=1, column=3, sticky='w', padx=10)

        # row 2: file 2 button + label
        self.file_two = StringVar(value='Select a file')
        self.file_two_entry = ttk.Entry(homepage, width=80, textvariable=self.file_two, state=DISABLED)
        self.file_two_entry.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)
        self.file_two_button = ttk.Button(homepage, text="Old File", command=self.load_file_two)
        self.file_two_button.grid(row=2, column=3, sticky='w', padx=10)
        self.file_two_button['state'] = DISABLED

        # row 3: run_allspice button
        image = Image.open(path_to_image)
        image = image.resize((40, 40), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.compare_button = ttk.Button(homepage, text="Show Diff", image=self.img, compound=LEFT,
                                         command=self.run_allspice, state=DISABLED)
        self.compare_button.grid(column=1, row=3, columnspan=3)

    def load_file_one(self):
        if path.isdir("D:\\SVN\\Engineering\\ECAD\\PRJ129\\PRJ129-2053-00"):
            initial_dir = "D:\\SVN\\Engineering\\ECAD\\PRJ129\\PRJ129-2053-00"
        else:
            initial_dir = path.expanduser('~')

        file_types = (('PCB Files', '*.schdoc *.SchDoc *.pcbdoc *.PcbDoc *.csv *.CSV'),
                      ('All files', '*.*'))

        filename = fd.askopenfilename(title='Select a file', initialdir=initial_dir,
                                      filetypes=file_types)
        if filename:
            self.file_one.set(filename)
            self.file_one_entry['state'] = NORMAL
            self.file_two_button['state'] = NORMAL
            self.compare_button['state'] = NORMAL
            self.tool_menu.entryconfigure(1, state=NORMAL)

    def load_file_two(self):
        file_types = (('PCB Files', '*.schdoc *.SchDoc *.pcbdoc *.PcbDoc *.csv *.CSV'),
                      ('All files', '*.*'))

        filename = fd.askopenfilename(title='Select a file', initialdir=path.dirname(self.file_one.get()),
                                      filetypes=file_types)
        if filename:
            self.file_two.set(filename)
            self.file_two_entry['state'] = NORMAL

    def run_allspice(self):
        try:
            if path.exists(self.file_two.get()):
                subprocess.run(['AllSpice', '--show', self.file_one.get(), '--diff', self.file_two.get()],
                               shell=True, check=True)
            else:
                subprocess.run(['AllSpice', '--show', self.file_one.get()], shell=True, check=True)
        except subprocess.CalledProcessError:
            ms.showerror("AllSpice Diff Not Found",
                         "Please make sure AllSpice Diff is installed and added to your PATH.")

    def clear_files(self):
        self.file_one.set("File cleared")
        self.file_one_entry['state'] = DISABLED
        self.file_two.set("File cleared")
        self.file_two_entry['state'] = DISABLED
        self.file_two_button['state'] = DISABLED
        self.compare_button['state'] = DISABLED
        self.tool_menu.entryconfigure(1, state=DISABLED)


if __name__ == '__main__':
    root = Tk()
    HomePage(root)
    root.mainloop()
