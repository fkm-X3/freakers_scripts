import os
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

class PowerControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Power Control Panel")
        self.root.geometry("420x370")
        self.root.resizable(False, False)

        self.action = tk.StringVar(value="shutdown")
        self.scheduled = False
        self.remaining_time = 0
        self.total_time = 0
        self.timer_thread = None

        # --- Widgets ---
        tk.Label(root, text="Schedule Power Action (minutes):", font=("Segoe UI", 11)).pack(pady=10)
        self.time_entry = tk.Entry(root, font=("Segoe UI", 11), justify="center")
        self.time_entry.pack(pady=5)

        tk.Label(root, text="Select Action:", font=("Segoe UI", 11)).pack(pady=5)
        actions_frame = tk.Frame(root)
        actions_frame.pack(pady=5)

        tk.Radiobutton(actions_frame, text="Shutdown", variable=self.action, value="shutdown").pack(side="left", padx=10)
        tk.Radiobutton(actions_frame, text="Restart", variable=self.action, value="restart").pack(side="left", padx=10)
        tk.Radiobutton(actions_frame, text="Hibernate", variable=self.action, value="hibernate").pack(side="left", padx=10)

        # Buttons
        self.start_btn = tk.Button(root, text="Start Timer", command=self.start_action, width=25)
        self.start_btn.pack(pady=5)

        self.skip_btn = tk.Button(root, text="Skip Timer (Do Now)", command=self.skip_timer, width=25)
        self.skip_btn.pack(pady=5)

        self.cancel_btn = tk.Button(root, text="Cancel Action", command=self.cancel_action, state="disabled", width=25)
        self.cancel_btn.pack(pady=5)

        self.status_label = tk.Label(root, text="No action scheduled.", font=("Segoe UI", 10))
        self.status_label.pack(pady=10)

        # Progress bar below timer
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def start_action(self):
        if self.scheduled:
            messagebox.showinfo("Already Scheduled", "An action is already scheduled.")
            return

        try:
            minutes = float(self.time_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")
            return

        seconds = int(minutes * 60)
        if seconds <= 0:
            messagebox.showerror("Invalid Time", "Please enter a positive number.")
            return

        self.total_time = seconds
        self.remaining_time = seconds
        self.scheduled = True
        self.cancel_btn.config(state="normal")
        self.start_btn.config(state="disabled")
        self.progress["value"] = 0
        self.progress["maximum"] = self.total_time

        selected_action = self.action.get()
        if selected_action == "shutdown":
            os.system(f"shutdown /s /t {seconds}")
        elif selected_action == "restart":
            os.system(f"shutdown /r /t {seconds}")
        elif selected_action == "hibernate":
            # Hibernate will be done manually after countdown
            pass

        self.status_label.config(text=f"{selected_action.capitalize()} in {minutes:.2f} minutes.")
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()

    def update_timer(self):
        while self.scheduled and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.status_label.config(
                text=f"{self.action.get().capitalize()} in {mins:02d}:{secs:02d}"
            )
            self.progress["value"] = self.total_time - self.remaining_time
            time.sleep(1)
            self.remaining_time -= 1

        if self.remaining_time <= 0 and self.scheduled:
            if self.action.get() == "hibernate":
                os.system("shutdown /h")
            self.status_label.config(text=f"{self.action.get().capitalize()} executing...")
            self.progress["value"] = self.total_time

    def cancel_action(self):
        if not self.scheduled:
            return

        os.system("shutdown /a")  # Abort shutdown or restart
        self.reset_state("Action canceled.")

    def skip_timer(self):
        """Immediately execute the selected action."""
        if self.scheduled:
            self.cancel_action()

        selected_action = self.action.get()
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to {selected_action} now?")
        if not confirm:
            return

        if selected_action == "shutdown":
            os.system("shutdown /s /t 0")
        elif selected_action == "restart":
            os.system("shutdown /r /t 0")
        elif selected_action == "hibernate":
            os.system("shutdown /h")

        self.reset_state(f"{selected_action.capitalize()} initiated.")

    def reset_state(self, message):
        """Resets UI state after canceling or skipping."""
        self.scheduled = False
        self.remaining_time = 0
        self.progress["value"] = 0
        self.cancel_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerControlPanel(root)
    root.mainloop()