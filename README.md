# Task Management REST API (FastAPI + SQLite)

A clean, production-ready, beginner-friendly Task Management REST API built with **Python 3.10+**, **FastAPI**, and **SQLite** persistent database storage. Designed for the **FlyRank Backend Track (Assignment 2)**.

---

## 🚀 Features

- **FastAPI Framework**: Blazing-fast performance, automatic request validation, and OpenAPI schema generation.
- **SQLite Database Integration**: Persistent storage in `tasks.db` using Python's native `sqlite3` library.
- **Automatic Initialization**: Database file, `tasks` table schema, and initial sample tasks are automatically created on server startup if missing.
- **RESTful API Principles**: Strict compliance with HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) and standard status codes (`200`, `201`, `204`, `400`, `404`).
- **Interactive OpenAPI Documentation**: Built-in Swagger UI available at `/docs`.
- **Strict Input Validation**: Pydantic validators reject empty or whitespace-only titles with `400 Bad Request`.

---

## 🗄️ Database Architecture & Why SQLite Was Chosen

### Why SQLite Was Chosen
- **Serverless & Zero-Configuration**: SQLite operates directly on disk without requiring complex database server setup, daemon processes, or user authentication configurations.
- **Built-in Python Support**: Python includes native support for SQLite via the standard `sqlite3` module, avoiding third-party driver compilation issues.
- **ACID Compliance & Data Persistence**: Ensures data durability across server restarts with high performance for local REST applications.

### Where `tasks.db` is Stored
The SQLite database file `tasks.db` is stored directly at the root of the project workspace:
```text
FlyRank_Intern/tasks.db
```

### How the Database is Automatically Created
When the server starts up (via `SQLiteTaskDatabase` initialization in `app/database.py`):
1. **File Creation**: Connects to `tasks.db`. SQLite automatically creates the file if it does not exist.
2. **Table Schema Creation**: Executes the query:
   ```sql
   CREATE TABLE IF NOT EXISTS tasks (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       done INTEGER NOT NULL
   );
   ```
3. **Sample Data Seeding**: Checks row count via `SELECT COUNT(*) FROM tasks;`. If the table is empty (`count == 0`), it automatically inserts exactly three initial sample tasks.

---

## 📁 Project Structure

```text
FlyRank_Intern/
├── app/
│   ├── __init__.py       # Package initializer
│   ├── main.py          # FastAPI application & REST endpoint handlers
│   ├── models.py        # Pydantic data schemas & request payload validators
│   └── database.py      # SQLite database connection, initialization, and CRUD operations
├── docs/                 # Documentation assets and screenshots
│   └── sqlite_screenshot.png  # Place your SQLite database GUI/CLI screenshot here
├── tasks.db              # SQLite database file (auto-created on startup)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation & API guide
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python **3.10+** installed on your system.

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/FlyRank_Intern.git
cd FlyRank_Intern

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Server

Start the development server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The server will start and automatically initialize `tasks.db` at **`http://127.0.0.1:8000`**.

---

## 📚 API Endpoints & Reference

Interactive Swagger UI documentation is live at **`http://127.0.0.1:8000/docs`**.

| Method | Endpoint | Description | SQL Query Executed | Status Code | Error Status |
|---|---|---|---|---|---|
| `GET` | `/` | API Metadata & Endpoint list | N/A | `200 OK` | N/A |
| `GET` | `/health` | Health Check | N/A | `200 OK` | N/A |
| `GET` | `/tasks` | List all tasks | `SELECT * FROM tasks;` | `200 OK` | N/A |
| `GET` | `/tasks/{id}` | Get task by ID | `SELECT * FROM tasks WHERE id = ?;` | `200 OK` | `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `INSERT INTO tasks (title, done) VALUES (?, ?);` | `201 Created` | `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title/done | `UPDATE tasks SET title = ?, done = ? WHERE id = ?;` | `200 OK` | `400 Bad Request` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `DELETE FROM tasks WHERE id = ?;` | `204 No Content` | `404 Not Found` |

---

## 💡 Example SQL Query

Here is an example SQL query used to select all pending tasks from the database:

```sql
SELECT * FROM tasks WHERE done = 0;
```

---

## 🖼️ Database Screenshot Location

Place your SQLite screenshot (e.g. from DB Browser for SQLite or VS Code SQLite extension showing `tasks.db` tables and rows) at:
```text
docs/sqlite_screenshot.png
```

![SQLite Database Screenshot](docs/sqlite_screenshot.png)

*(Note: Replace `docs/sqlite_screenshot.png` with your actual screenshot file path once captured).*

---

## 📄 License

Distributed under the MIT License. Built for FlyRank Backend Track (Assignment 2).
