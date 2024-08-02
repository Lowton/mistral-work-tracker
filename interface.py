import tkinter as tk
from tkinter import messagebox
from datetime import timedelta
from timer import WorkTimer
from database import WorkTimeDatabase

class WorkTimeApp:
    def __init__(self, root: tk.Tk, db: WorkTimeDatabase, timer: WorkTimer):
        self.root = root
        self.root.title("Work Time Tracker")

        self.db = db
        self.timer = timer

        self.time_label = tk.Label(root, text=self.format_time(self.timer.get_remaining_time()), font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.update_time()

    def start_timer(self) -> None:
        self.timer.start()
        self.update_time()

    def pause_timer(self) -> None:
        self.timer.pause()
        self.update_time()

    def stop_timer(self) -> None:
        self.timer.stop()
        self.update_time()
        messagebox.showinfo("Work Time", f"Total work time: {self.format_time(self.timer.get_total_work_time())}")

    def update_time(self) -> None:
        remaining_time = self.timer.get_remaining_time()
        self.time_label.config(text=self.format_time(remaining_time))
        if remaining_time.total_seconds() <= 0:
            self.time_label.config(fg="red")
        else:
            self.time_label.config(fg="black")
        self.root.after(1000, self.update_time)

    def format_time(self, time: timedelta) -> str:
        total_seconds = int(time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
