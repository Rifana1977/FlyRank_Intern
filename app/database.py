import sqlite3
import os
from typing import List, Optional, Dict, Any
from app.models import Task, TaskCreate, TaskUpdate

# Path to SQLite database file in the project root directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.db")


class SQLiteTaskDatabase:
    """
    SQLite task database store using Python's built-in sqlite3 module.
    Manages tasks.db initialization, table creation, and sample task insertion.
    """
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """
        Creates and returns a SQLite connection with Row factory.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """
        Initializes the database:
        - Creates tasks.db if missing
        - Creates tasks table if missing
        - Inserts exactly 3 sample tasks ONLY if the table is empty
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Create table if missing
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL
                );
            """)
            
            # 2. Check if table is empty
            cursor.execute("SELECT COUNT(*) FROM tasks;")
            count = cursor.fetchone()[0]
            
            # 3. Insert sample tasks if table is empty
            if count == 0:
                sample_tasks = [
                    ("Buy groceries", 0),
                    ("Complete Assignment 2", 0),
                    ("Read SQLite documentation", 0)
                ]
                cursor.executemany(
                    "INSERT INTO tasks (title, done) VALUES (?, ?);",
                    sample_tasks
                )
                conn.commit()

    def get_all(self) -> List[Task]:
        """
        GET /tasks implementation: Executes `SELECT * FROM tasks`.
        Returns all task records from SQLite tasks table.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks;")
            rows = cursor.fetchall()
            return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        GET /tasks/:id implementation: Executes `SELECT * FROM tasks WHERE id = ?`.
        Returns a single task record or None if the ID is not found.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?;", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def create(self, task_data: TaskCreate) -> Task:
        """
        POST /tasks implementation: Executes `INSERT INTO tasks (title, done) VALUES (?, ?);`.
        Inserts new task record into SQLite database with done=0, fetches lastrowid,
        and returns the created Task object.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?);", (task_data.title, 0))
            conn.commit()
            task_id = cursor.lastrowid
            return Task(id=task_id, title=task_data.title, done=False)

    def update(self, task_id: int, update_data: TaskUpdate) -> Optional[Task]:
        """
        PUT /tasks/:id implementation: Executes `UPDATE tasks SET title = ?, done = ? WHERE id = ?;`.
        Updates fields for existing task row in SQLite database and returns updated Task object,
        or None if task ID is not found.
        """
        existing = self.get_by_id(task_id)
        if existing is None:
            return None
        new_title = update_data.title if update_data.title is not None else existing.title
        new_done = int(update_data.done) if update_data.done is not None else int(existing.done)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?;", (new_title, new_done, task_id))
            conn.commit()
        return Task(id=task_id, title=new_title, done=bool(new_done))

    def delete(self, task_id: int) -> bool:
        """
        DELETE /tasks/:id implementation: Executes `DELETE FROM tasks WHERE id = ?;`.
        Deletes task row from SQLite database. Returns True if row was deleted, False if ID not found.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
            conn.commit()
            return cursor.rowcount > 0


# Singleton database instance shared across the application
from app.postgres_repository import PostgresTaskRepository

db = PostgresTaskRepository()

