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
            timestamp TEXT NOT NULL,
            session_time TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def save_action(self, action: str, session_time: timedelta) -> None:
        """Сохранение действия в базу данных."""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO work_time (action, timestamp, session_time) VALUES (?, ?, ?)',
                            (action, current_time, str(session_time)))
        self.conn.commit()
        print(f'Action saved: {action} at {current_time} with session time {session_time}')

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
        self.cursor.execute('SELECT session_time FROM work_time WHERE action = "stop" AND DATE(timestamp) = ?', (today,))
        session_times = self.cursor.fetchall()

        total_work_time = timedelta()
        for session_time in session_times:
            total_work_time += timedelta(hours=int(session_time[0].split(':')[0]),
                                           minutes=int(session_time[0].split(':')[1]),
                                           seconds=int(session_time[0].split(':')[2]))

        return total_work_time

    def get_total_overtime(self) -> timedelta:
        """Получение общей переработки или недоработки за все предыдущие рабочие дни."""
        self.cursor.execute('SELECT DATE(timestamp) FROM work_time WHERE action = "stop" GROUP BY DATE(timestamp)')
        work_days = self.cursor.fetchall()

        total_overtime = timedelta()
        for work_day in work_days:
            work_day_date = work_day[0]
            self.cursor.execute('SELECT session_time FROM work_time WHERE action = "stop" AND DATE(timestamp) = ?', (work_day_date,))
            session_times = self.cursor.fetchall()

            total_work_time = timedelta()
            for session_time in session_times:
                total_work_time += timedelta(hours=int(session_time[0].split(':')[0]),
                                               minutes=int(session_time[0].split(':')[1]),
                                               seconds=int(session_time[0].split(':')[2]))

            expected_work_time = timedelta(hours=8)
            overtime = total_work_time - expected_work_time
            total_overtime += overtime

        return total_overtime

    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        self.conn.close()
