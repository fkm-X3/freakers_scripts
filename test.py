import tkinter as tk

def center_window(window, width, height):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate x and y coordinates for the window's top-left corner
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the window's geometry
    window.geometry(f'{width}x{height}+{x}+{y}')

# Example usage:
root = tk.Tk()
root.title("Centered Tkinter Window")

# Define desired window dimensions
window_width = 800
window_height = 500

# Center the window
center_window(root, window_width, window_height)

root.mainloop()