import time
from datetime import datetime, timedelta
from typing import Optional

class WorkTimer:
    def __init__(self, db, initial_time: timedelta = timedelta(hours=8)):
        self.db = db
        self.initial_time = initial_time
        self.remaining_time = initial_time
        self.is_running = False
        self.start_time: Optional[datetime] = None
        self.total_work_time = timedelta()

    def start(self) -> None:
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now()
            self.db.save_action("start")

    def pause(self) -> None:
        if self.is_running:
            self.is_running = False
            elapsed_time = datetime.now() - self.start_time
            self.remaining_time -= elapsed_time
            self.total_work_time += elapsed_time
            self.db.save_action("pause")

    def stop(self) -> None:
        if self.is_running:
            self.pause()
        self.db.save_action("stop")

    def get_remaining_time(self) -> timedelta:
        if self.is_running:
            elapsed_time = datetime.now() - self.start_time
            return self.remaining_time - elapsed_time
        return self.remaining_time

    def get_total_work_time(self) -> timedelta:
        if self.is_running:
            elapsed_time = datetime.now() - self.start_time
            return self.total_work_time + elapsed_time
        return self.total_work_time

    def reset(self) -> None:
        self.remaining_time = self.initial_time
        self.is_running = False
        self.start_time = None
        self.total_work_time = timedelta()
