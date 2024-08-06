import sqlite3
from datetime import datetime, timedelta
from typing import Optional

"""
Модуль для работы с базой данных SQLite.

Этот модуль предоставляет класс WorkTimeDatabase, который управляет сохранением и извлечением данных о рабочем времени в базе данных SQLite.
"""

class WorkTimeDatabase:
    """Класс для работы с базой данных SQLite."""

    def __init__(self, db_name: str = 'work_time.db'):
        """Инициализация базы данных."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        """Создание таблицы в базе данных."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_time (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def save_action(self, action: str) -> None:
        """Сохранение действия в базу данных."""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO work_time (action, timestamp) VALUES (?, ?)',
                            (action, current_time))
        self.conn.commit()
        print(f'Action saved: {action} at {current_time}')

    def get_last_work_day(self) -> Optional[datetime]:
        """Получение последнего рабочего дня."""
        self.cursor.execute('SELECT timestamp FROM work_time WHERE action = "stop" ORDER BY timestamp DESC LIMIT 1')
        result = self.cursor.fetchone()
        if result:
            return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        return None

    def get_today_work_time(self) -> timedelta:
        """Получение общего рабочего времени за сегодня."""
        today = datetime.now().date()
        self.cursor.execute('SELECT timestamp FROM work_time WHERE action = "start" AND DATE(timestamp) = ?', (today,))
        start_times = self.cursor.fetchall()
        self.cursor.execute('SELECT timestamp FROM work_time WHERE action = "pause" AND DATE(timestamp) = ?', (today,))
        pause_times = self.cursor.fetchall()

        total_work_time = timedelta()
        for start_time in start_times:
            start_dt = datetime.strptime(start_time[0], '%Y-%m-%d %H:%M:%S')
            for pause_time in pause_times:
                pause_dt = datetime.strptime(pause_time[0], '%Y-%m-%d %H:%M:%S')
                if pause_dt > start_dt:
                    total_work_time += (pause_dt - start_dt)
                    break

        return total_work_time

    def get_last_work_day_overtime(self) -> timedelta:
        """Получение переработки или недоработки за последний рабочий день."""
        last_work_day = self.get_last_work_day()
        if not last_work_day:
            return timedelta()

        last_work_day_date = last_work_day.date()
        self.cursor.execute('SELECT timestamp FROM work_time WHERE action = "start" AND DATE(timestamp) = ?', (last_work_day_date,))
        start_times = self.cursor.fetchall()
        self.cursor.execute('SELECT timestamp FROM work_time WHERE action = "pause" AND DATE(timestamp) = ?', (last_work_day_date,))
        pause_times = self.cursor.fetchall()

        total_work_time = timedelta()
        for start_time in start_times:
            start_dt = datetime.strptime(start_time[0], '%Y-%m-%d %H:%M:%S')
            for pause_time in pause_times:
                pause_dt = datetime.strptime(pause_time[0], '%Y-%m-%d %H:%M:%S')
                if pause_dt > start_dt:
                    total_work_time += (pause_dt - start_dt)
                    break

        expected_work_time = timedelta(hours=8)
        overtime = total_work_time - expected_work_time
        return overtime

    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        self.conn.close()
