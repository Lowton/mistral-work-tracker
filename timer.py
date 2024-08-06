from datetime import datetime, timedelta
from typing import Optional

"""
Модуль для работы с таймером.

Этот модуль предоставляет класс WorkTimer, который управляет таймером для отслеживания рабочего времени.
"""

class WorkTimer:
    """Класс для работы с таймером."""

    def __init__(self, db, initial_time: timedelta = timedelta(hours=8)):
        """Инициализация таймера."""
        self.db = db
        self.initial_time = initial_time
        self.remaining_time = initial_time
        self.is_running = False
        self.start_time: Optional[datetime] = None
        self.total_work_time = timedelta()

    def start(self) -> None:
        """Запуск таймера."""
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now()
            self.db.save_action("start", timedelta())

    def pause(self) -> None:
        """Пауза таймера."""
        if self.is_running:
            self.is_running = False
            elapsed_time = datetime.now() - self.start_time
            self.remaining_time -= elapsed_time
            self.total_work_time += elapsed_time
            self.db.save_action("pause", elapsed_time)

    def stop(self) -> None:
        """Остановка таймера."""
        if self.is_running:
            self.pause()
        self.db.save_action("stop", self.total_work_time)

    def get_remaining_time(self) -> timedelta:
        """Получение оставшегося времени."""
        if self.is_running:
            elapsed_time = datetime.now() - self.start_time
            return self.remaining_time - elapsed_time
        return self.remaining_time

    def get_total_work_time(self) -> timedelta:
        """Получение общего рабочего времени."""
        if self.is_running:
            elapsed_time = datetime.now() - self.start_time
            return self.total_work_time + elapsed_time
        return self.total_work_time

    def reset(self) -> None:
        """Сброс таймера."""
        self.remaining_time = self.initial_time
        self.is_running = False
        self.start_time = None
        self.total_work_time = timedelta()
