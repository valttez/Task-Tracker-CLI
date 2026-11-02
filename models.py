from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str

    VALID_STATUSES = ("todo", "in-progress", "done")

    @classmethod
    def create(cls, task_id: int, descr: str) -> "Task":
        now = datetime.now().isoformat(timespec="seconds")
        return cls(
            id=task_id,
            description=descr,
            status="todo",
            createdAt=now,
            updatedAt=now
        )

    def change_status(self, status: str) -> None:
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Недопустимый статус {status}")
        self.updatedAt = datetime.now().isoformat(timespec="seconds")
        self.status = status

    def update_description(self, descr: str) -> None:
        self.description = descr
        self.updatedAt = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id = data["id"],
            description=data["description"],
            status= data["status"],
            createdAt = data["createdAt"],
            updatedAt = data["updatedAt"]
        )


