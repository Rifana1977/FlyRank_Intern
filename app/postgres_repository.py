import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from dotenv import load_dotenv
from app.models import Task, TaskCreate, TaskUpdate

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "taskdb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


class PostgresTaskRepository:
    """
    PostgreSQL Task Repository using psycopg2 with parameterized SQL queries.
    Implements the exact same interface contract as the repository:
    - get_all() / getAll()
    - get_by_id(id) / getById(id)
    - create(task)
    - update(id, data)
    - delete(id)
    """

    def __init__(self, connection_url: str = DATABASE_URL) -> None:
        self.connection_url = connection_url

    def get_connection(self):
        """
        Creates and returns a PostgreSQL connection with RealDictCursor for dict-like row access.
        """
        return psycopg2.connect(self.connection_url, cursor_factory=RealDictCursor)

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks from PostgreSQL tasks table.
        SQL: SELECT id, title, done FROM tasks ORDER BY id ASC;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
                rows = cursor.fetchall()
                return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a single task by ID using parameterized SQL query (%s).
        SQL: SELECT id, title, done FROM tasks WHERE id = %s;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
                row = cursor.fetchone()
                if row is None:
                    return None
                return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def create(self, task_data: TaskCreate) -> Task:
        """
        Inserts a new task row into PostgreSQL and returns the created Task object.
        SQL: INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                    (task_data.title, False)
                )
                row = cursor.fetchone()
                conn.commit()
                return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def update(self, task_id: int, update_data: TaskUpdate) -> Optional[Task]:
        """
        Updates an existing task by ID using parameterized SQL query.
        SQL: UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;
        """
        existing = self.get_by_id(task_id)
        if existing is None:
            return None

        new_title = update_data.title if update_data.title is not None else existing.title
        new_done = update_data.done if update_data.done is not None else existing.done

        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                    (new_title, new_done, task_id)
                )
                row = cursor.fetchone()
                conn.commit()
                if row is None:
                    return None
                return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def delete(self, task_id: int) -> bool:
        """
        Deletes a task by ID using parameterized SQL query.
        SQL: DELETE FROM tasks WHERE id = %s RETURNING id;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
                row = cursor.fetchone()
                conn.commit()
                return row is not None

    # Alias methods for snake_case and camelCase method signature compatibility
    def getAll(self) -> List[Task]:
        return self.get_all()

    def getById(self, task_id: int) -> Optional[Task]:
        return self.get_by_id(task_id)
