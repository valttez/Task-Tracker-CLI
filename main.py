import sys
from repo import TaskRepository
from models import Task

class TaskCLI:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def run(self, argv: list[str]) -> None:
        if len(argv) < 2:
            self.show_help()
            return

        command = argv[1]
        args = argv[2:]

        try:
            match command:
                case "add":
                    self._add(args)
                case "update":
                    self._update(args)
                case "delete":
                    self._delete(args)
                case "mark-in-progress":
                    self._set_status(args, "in-progress")
                case "mark-done":
                    self._set_status(args, "done")
                case "list":
                    self._list(args)
                case "-h" | "--help" | "help":
                    self.show_help()
                case _:
                    print(f"Неизвестная команда: {command}\n", file=sys.stderr)
                    self.show_help()
                    sys.exit(1)
        except (ValueError, KeyError) as err:
            print(f"Ошибка: {err}", file=sys.stderr)
            sys.exit(1)

    def _add(self, args: list[str]) -> None:
        if not args or not args[0].strip():
            raise ValueError("Укажите непустое описание задачи.")
        task = self.repo.add(args[0].strip())
        print(f"Task added successfully (ID: {task.id})")

    def _parse_id(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError("ID задачи должен быть целым числом.")

    def _update(self, args: list[str]) -> None:
        if len(args) < 2 or not args[1].strip():
            raise ValueError("Укажите ID и новое описание задачи.")
        task_id = self._parse_id(args[0])
        self.repo.update(task_id, args[1].strip())
        print(f"Task updated successfully (ID: {task_id})")

    def _delete(self, args: list[str]) -> None:
        if not args:
            raise ValueError("Укажите ID задачи.")
        task_id = self._parse_id(args[0])
        self.repo.delete(task_id)
        print(f"Task deleted successfully (ID: {task_id})")

    def _set_status(self, args: list[str], status: str) -> None:
        if not args:
            raise ValueError("Укажите ID задачи.")
        task_id = self._parse_id(args[0])
        self.repo.set_status(task_id, status)
        print(f"Task status changed to '{status}' (ID: {task_id})")

    def _list(self, args: list[str]) -> None:
        status = args[0] if args else None
        if status and status not in Task.VALID_STATUSES:
            raise ValueError(f"Неизвестный статус: '{status}'. Допустимые: {', '.join(Task.VALID_STATUSES)}")

        tasks = self.repo.list_tasks(status)
        if not tasks:
            print("Задачи не найдены.")
            return

        header = f"{'ID':<4} | {'Status':<12} | {'Description':<35} | {'Created At':<20} | {'Updated At':<20}"
        print(header)
        print("-" * len(header))
        for t in tasks:
            desc = t.description if len(t.description) <= 32 else t.description[:29] + "..."
            print(f"{t.id:<4} | {t.status:<12} | {desc:<35} | {t.createdAt:<20} | {t.updatedAt:<20}")



    @staticmethod
    def show_help() -> None:
        print("""Использование: task-cli <command> [аргументы]

Команды:
  add <description>             Добавить новую задачу
  update <id> <description>     Обновить описание задачи
  delete <id>                   Удалить задачу
  mark-in-progress <id>         Перевести в статус 'in-progress'
  mark-done <id>                Перевести в статус 'done'
  list                          Показать все задачи
  list <status>                 Фильтр по статусу (todo, in-progress, done)
""")


if __name__ == "__main__":
    cli = TaskCLI(TaskRepository("tasks.json"))
    cli.run(sys.argv)