import sys
import os
import ctypes
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess


def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showinfo("Info", "Already running as Administrator!")
        return
    else:
        # Relaunch the script with admin rights
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            # Optionally close the current window
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to relaunch as admin:\n{e}")

def Create_File():
    try:
        subprocess.run(["python", "File_creator.py"], shell=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "File_creator.py not found. Please ensure it is in the same directory.")

def Open_Steam():
    try:
        subprocess.run(["start", "steam://open/main"], shell=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "Steam isn't installed.")

def paint():
    try:
        subprocess.run(["python", "paint.py"], shell=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "Insure you have the paint.py script in the directory.")

def Power_Control():
    subprocess.run(["python", "Power_control_Panel.py"], shell=True)

def admin():
    admin = messagebox.askokcancel("Admin Rights", "Requesting admin rights...")
    if admin:
        run_as_admin()  
    else:
        messagebox.showwarning("Warning", "Admin rights request Denied.")


root = tk.Tk()
root.title("Sdiybt")
root.geometry("300x200")
frame = ttk.Frame(root)
frame.pack(side=tk.TOP)

admin_button = tk.Button(root, text="Admin Perms.", command=admin)
admin_button.pack(side=tk.TOP, pady=5)

create = tk.Button(root, text="Create File.", command=Create_File)
create.pack(side=tk.TOP, pady=5)

steam = tk.Button(root, text="Open Steam.", command=Open_Steam)
steam.pack(side=tk.TOP, pady=5)

WEB = tk.Button(root, text="MS Paint but worse.", command=paint)
WEB.pack(side=tk.TOP, pady=5)

shutdown = tk.Button(root, text='Power Control Panel.', command= Power_Control)
shutdown.pack(side=tk.TOP, pady=5)


root.mainloop()