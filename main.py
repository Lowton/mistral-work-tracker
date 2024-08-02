import tkinter as tk
from datetime import timedelta
from database import WorkTimeDatabase
from timer import WorkTimer
from interface import WorkTimeApp

def main():
    """Основная функция для запуска приложения."""
    root = tk.Tk()

    db = WorkTimeDatabase()
    last_work_day = db.get_last_work_day()
    today_work_time = db.get_today_work_time()

    if last_work_day:
        initial_time = timedelta(hours=8) - today_work_time
    else:
        initial_time = timedelta(hours=8)

    timer = WorkTimer(db, initial_time)

    app = WorkTimeApp(root, db, timer)
    root.mainloop()
    db.close()

if __name__ == "__main__":
    main()
