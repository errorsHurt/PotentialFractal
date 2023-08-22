from tkinter import *


def createWindow():
    root = Tk()
    root.title("Potential Fractals")
    root.geometry('1500x900')

    menubar = create_menu_bar(root)

    file_menu = create_menu(menubar, "File")
    create_menu_item(file_menu, "New")
    create_menu_item(file_menu, "Exit", root.quit)

    file_menu = create_menu(menubar, "Edit")
    file_menu = create_menu(menubar, "Help")

    root.mainloop()


def create_menu_item(file_menu: Menu, label: str, command=None):
    file_menu.add_command(label=label, command=command)


def create_menu(menubar: Menu, label: str):
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label=label, menu=file_menu)
    return file_menu


def create_menu_bar(root):
    menubar = Menu(root)
    root.config(menu=menubar)
    return menubar
