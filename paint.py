import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter Paint")

        self.color = "black"
        self.line_width = 2
        self.old_x, self.old_y = None, None

        # Create Canvas
        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)
        self.canvas.pack(expand=True, fill="both")

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Create control frame
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side="top", fill="x")

        # Color button
        self.color_button = tk.Button(self.control_frame, text="Color", command=self.choose_color)
        self.color_button.pack(side="left", padx=5)

        # Line width slider
        self.width_slider = tk.Scale(self.control_frame, from_=1, to=10, orient="horizontal", label="Width", command=self.change_width)
        self.width_slider.set(self.line_width)
        self.width_slider.pack(side="left", padx=5)

        # Clear button
        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side="left", padx=5)

    def start_draw(self, event):
        self.old_x, self.old_y = event.x, event.y

    def draw(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    fill=self.color, width=self.line_width,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.old_x, self.old_y = event.x, event.y

    def stop_draw(self, event):
        self.old_x, self.old_y = None, None

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[1]: # If a color was selected
            self.color = color_code[1]

    def change_width(self, val):
        self.line_width = int(val)

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()