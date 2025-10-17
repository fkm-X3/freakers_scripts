import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

root = Tk()
root.title("Untitled - Text Editor")
root.geometry('800x600')

text_area = Text(root, font=("Arial", 12))
text_area.pack(expand=True, fill=BOTH)

# track the currently open file (None means untitled/new)
current_file = None

scroller = Scrollbar(text_area, orient=VERTICAL)
scroller.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroller.set)
scroller.config(command=text_area.yview)

def open_file():
    global current_file
    file_path = fd.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text_area.delete(1.0, END)
                text_area.insert(1.0, file.read())
            current_file = file_path
            root.title(f"{file_path} - Text Editor")
        except Exception as e:
            mb.showerror("Open Error", str(e))

def new_file():
    global current_file
    text_area.delete(1.0, END)
    current_file = None
    root.title("Untitled - Text Editor")

def save_file():
    global current_file
    if current_file:
        try:
            with open(current_file, "w", encoding="utf-8") as file:
                file.write(text_area.get(1.0, END))
            root.title(f"{current_file} - Text Editor")
        except Exception as e:
            mb.showerror("Save Error", str(e))
    else:
        save_file_as()

def save_file_as():
    global current_file
    file_path = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get(1.0, END))
            current_file = file_path
            root.title(f"{current_file} - Text Editor")
        except Exception as e:
            mb.showerror("Save Error", str(e))

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file) # Assuming new_file function exists
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file) # Assuming save_file function exists
file_menu.add_command(label="Save As...", command=save_file_as) # Assuming save_file_as function exists
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()