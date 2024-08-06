import tkinter as tk
from datetime import datetime, timedelta
from database import WorkTimeDatabase
from timer import WorkTimer
from interface import WorkTimeApp

"""
Основной модуль для запуска приложения.

Этот модуль предоставляет основную функцию для запуска приложения Work Time Tracker.
"""

def main():
    """Основная функция для запуска приложения."""
    root = tk.Tk()

    db = WorkTimeDatabase()
    last_work_day = db.get_last_work_day()
    today_work_time = db.get_today_work_time()
    last_work_day_overtime = db.get_last_work_day_overtime()

    if last_work_day:
        initial_time = timedelta(hours=8) - today_work_time - last_work_day_overtime
    else:
        initial_time = timedelta(hours=8)

    timer = WorkTimer(db, initial_time)

    app = WorkTimeApp(root, db, timer)
    root.mainloop()
    db.close()

if __name__ == "__main__":
    main()
