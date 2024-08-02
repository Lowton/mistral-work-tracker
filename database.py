import sqlite3
from datetime import datetime, timedelta
from typing import Optional

class WorkTimeDatabase:
    def __init__(self, db_name: str = 'work_time.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_time (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def save_action(self, action: str) -> None:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO work_time (action, timestamp) VALUES (?, ?)', (action, current_time))
        self.conn.commit()
        print(f'Action saved: {action} at {current_time}')

    def get_last_work_day(self) -> Optional[datetime]:
        self.cursor.execute('SELECT timestamp FROM work_time WHERE action = "stop" ORDER BY timestamp DESC LIMIT 1')
        result = self.cursor.fetchone()
        if result:
            return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        return None

    def get_today_work_time(self) -> timedelta:
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

    def close(self) -> None:
        self.conn.close()
