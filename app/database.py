from typing import List, Optional
from app.models import Task, TaskCreate, TaskUpdate


class InMemoryTaskDatabase:
    """
    In-memory task database store using a Python list.
    No persistent database engine is used as per project requirements.
    """
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def get_all(self) -> List[Task]:
        """Returns all tasks currently stored in memory."""
        return self.tasks

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a single task by ID.
        Returns None if no task with the specified ID exists.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def create(self, task_data: TaskCreate) -> Task:
        """
        Creates a new Task object with auto-incremented ID and default done=False.
        Appends it to the in-memory list and returns the newly created Task.
        """
        new_task = Task(
            id=self._next_id,
            title=task_data.title,
            done=False
        )
        self._next_id += 1
        self.tasks.append(new_task)
        return new_task

    def update(self, task_id: int, update_data: TaskUpdate) -> Optional[Task]:
        """
        Updates an existing task in-place.
        Returns the updated Task object, or None if the task does not exist.
        """
        task = self.get_by_id(task_id)
        if task is None:
            return None

        if update_data.title is not None:
            task.title = update_data.title
        if update_data.done is not None:
            task.done = update_data.done

        return task

    def delete(self, task_id: int) -> bool:
        """
        Deletes a task by ID from the in-memory list.
        Returns True if deleted successfully, False if task ID was not found.
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False


# Singleton database instance shared across the application
db = InMemoryTaskDatabase()
