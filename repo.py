import json
import os
from models import Task

class TaskRepository:
    def __init__(self, filename: str = "tasks.json") -> None:
        self.filename = filename

    def load_all(self) -> list[Task]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError):
            return []

    def save_all(self, tasks: list[Task]) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            data = [task.to_dict() for task in tasks]
            json.dump(data, file, indent=2, ensure_ascii=False)

    def get_next_id(self, tasks: list[Task]) -> int:
        return max((t.id for t in tasks), default= 0) + 1

    def add(self, description: str) -> Task:
        tasks = self.load_all()
        new_task = Task.create(self.get_next_id(tasks), description)
        tasks.append(new_task)
        self.save_all(tasks)
        return new_task

    def get(self, task_id: int) -> Task | None:
        tasks = self.load_all()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id: int, descr: str) -> Task:
        tasks = self.load_all()
        for task in tasks:
            if task.id == task_id:
                task.update_description(descr)
                self.save_all(tasks)
                return task
        raise KeyError(f"Задача с ID {task_id} не найдена!")

    def set_status(self, task_id: int, status: str) -> Task:
        tasks = self.load_all()
        for task in tasks:
            if task.id == task_id:
                task.change_status(status)
                self.save_all(tasks)
                return task
        raise KeyError(f"Задача с ID {task_id} не найдена!")

    def delete(self, task_id: int) -> None:
        tasks = self.load_all()
        filtered = [t for t in tasks if t.id != task_id]
        if len(filtered) == len(tasks):
            raise KeyError(f"Задача с ID {task_id} не найдена!")
        self.save_all(filtered)

    def list_tasks(self, status: str | None = None) -> list[Task]:
        tasks = self.load_all()
        if status:
            return [t for t in tasks if t.status == status]
        return tasks
