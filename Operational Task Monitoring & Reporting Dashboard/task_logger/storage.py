import json
from pathlib import Path
from datetime import date
from typing import List, Optional
from .models import Task

class TaskStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        self.tasks: List[Task] = []
        self.load()

    def load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
            except Exception:
                self.tasks = []
        else:
            self.tasks = []

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save()

    def get_all(self, status: Optional[str] = None):
        if status is None:
            return self.tasks[:]
        return [t for t in self.tasks if t.status == status]

    def mark_complete(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                task.status = "completed"
                task.completed_date = str(date.today())
                self.save()
                return True
        return False

    def get_next_id(self) -> int:
        return max((t.id for t in self.tasks), default=0) + 1
