# Task Management REST API (FastAPI + SQLite)

A clean, production-ready, beginner-friendly Task Management REST API built with **Python 3.10+**, **FastAPI**, and **SQLite** persistent database storage. Designed for the **FlyRank Backend Track (Week 2 & Assignment 2)**.

---

## 🚀 Features

- **FastAPI Framework**: Blazing-fast performance, automatic request validation, and OpenAPI schema generation.
- **SQLite Database Integration**: Persistent data storage using Python's native `sqlite3` library in `tasks.db`.
- **Automatic Database Initialization**: Database file, `tasks` table schema, and initial sample tasks are automatically created on server startup if missing.
- **RESTful API Principles**: Strict compliance with standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) and standard status codes (`200`, `201`, `204`, `400`, `404`).
- **Interactive OpenAPI Documentation**: Built-in Swagger UI available at `/docs`.
- **Input Validation**: Strict request payload validation using Pydantic models (empty or whitespace-only titles are rejected with `400 Bad Request`).
- **Type Hinting**: Clean, fully typed Python code throughout models, database access, and endpoint handlers.

---

## 🗄️ Database Architecture & SQLite Integration

### Why SQLite Was Chosen
- **Serverless & Zero-Configuration**: SQLite operates directly on disk without requiring complex database server setup, background daemons, or authentication configuration.
- **Native Python Standard Library**: Python includes built-in support for SQLite via the standard `sqlite3` module, avoiding external dependency conflicts.
- **ACID Compliance & Persistence**: Provides lightweight yet reliable ACID transaction support, guaranteeing data persistence across server restarts.

### Where `tasks.db` is Stored
The SQLite database file `tasks.db` is stored at the root of the workspace:
```text
FlyRank_Intern/tasks.db
```

### How the Database is Automatically Created
When the server starts up (`SQLiteTaskDatabase` instance in `app/database.py`):
1. **File Creation**: Connects to `tasks.db`. SQLite creates the database file automatically if missing.
2. **Table Schema Creation**: Executes the table creation query:
   ```sql
   CREATE TABLE IF NOT EXISTS tasks (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       done INTEGER NOT NULL
   );
   ```
3. **Sample Tasks Seeding**: Checks current row count via `SELECT COUNT(*) FROM tasks;`. If the table is empty (`count == 0`), it automatically inserts exactly three sample tasks:
   - `("Buy groceries", 0)`
   - `("Complete Assignment 2", 0)`
   - `("Read SQLite documentation", 0)`

---

## 📁 Project Structure

```text
FlyRank_Intern/
├── app/
│   ├── __init__.py       # Package initializer
│   ├── main.py          # FastAPI application & REST endpoint handlers
│   ├── models.py        # Pydantic data schemas & payload validators
│   └── database.py      # SQLite connection, startup initialization & CRUD operations
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
The server will start at **`http://127.0.0.1:8000`**. On startup, `tasks.db` is initialized automatically.

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
| `PUT` | `/tasks/{id}` | Update task title/status | `UPDATE tasks SET title = ?, done = ? WHERE id = ?;` | `200 OK` | `400 Bad Request` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `DELETE FROM tasks WHERE id = ?;` | `204 No Content` | `404 Not Found` |

---

### Request & Response Examples

#### 1. Root Endpoint (`GET /`)
- **Response `200 OK`**:
```json
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks"]
}
```

#### 2. Health Check (`GET /health`)
- **Response `200 OK`**:
```json
{
  "status": "ok"
}
```

#### 3. List All Tasks (`GET /tasks`)
- **Response `200 OK`**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "done": false
  },
  {
    "id": 2,
    "title": "Complete Assignment 2",
    "done": false
  },
  {
    "id": 3,
    "title": "Read SQLite documentation",
    "done": false
  }
]
```

#### 4. Create Task (`POST /tasks`)
- **Request Body**:
```json
{
  "title": "Buy milk"
}
```
- **Response `201 Created`**:
```json
{
  "id": 4,
  "title": "Buy milk",
  "done": false
}
```
- **Invalid Payload (Missing/Empty Title) -> `400 Bad Request`**:
```json
{
  "error": "Title cannot be empty"
}
```

#### 5. Get Task by ID (`GET /tasks/1`)
- **Response `200 OK`**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "done": false
}
```
- **Task Not Found -> `404 Not Found`**:
```json
{
  "error": "Task not found"
}
```

#### 6. Update Task (`PUT /tasks/1`)
- **Request Body**:
```json
{
  "title": "Buy organic groceries",
  "done": true
}
```
- **Response `200 OK`**:
```json
{
  "id": 1,
  "title": "Buy organic groceries",
  "done": true
}
```
- **Task Not Found -> `404 Not Found`**:
```json
{
  "error": "Task not found"
}
```

#### 7. Delete Task (`DELETE /tasks/1`)
- **Response `204 No Content`** *(Empty body)*
- **Task Not Found -> `404 Not Found`**:
```json
{
  "error": "Task not found"
}
```

---

## 💡 SQL Query Reference & Explanations

Here are the key SQL queries used in the application and what each one does:

1. **`SELECT * FROM tasks;`**
   - *Description*: Retrieves all columns (`id`, `title`, `done`) for all rows in the `tasks` table. Used by `GET /tasks`.

2. **`SELECT * FROM tasks WHERE done = 1;`**
   - *Description*: Filters and returns all task rows where `done = 1` (completed tasks).

3. **`SELECT COUNT(*) FROM tasks;`**
   - *Description*: Counts the total number of rows in the `tasks` table. Used on startup to check if the database is empty before seeding sample tasks.

4. **`UPDATE tasks SET done = 1;`**
   - *Description*: Updates the `done` status column to `1` (completed) for all tasks in the table unconditionally.

5. **`DELETE FROM tasks WHERE done = 1;`**
   - *Description*: Removes all task rows from the table where `done = 1` (deleting all completed tasks).

6. **`SELECT * FROM tasks WHERE done = 0;`**
   - *Description*: Selects all pending/uncompleted tasks (`done = 0`).

---

## 🖼️ Database Screenshot Location

Place your SQLite database GUI/CLI screenshot (e.g. from DB Browser for SQLite or VS Code SQLite Viewer) at:
```text
docs/sqlite_screenshot.png
```

![SQLite Database Screenshot](docs/sqlite_screenshot.png)

---

## 🧪 Testing with cURL / Postman / Swagger UI

### Using Interactive Swagger UI
Navigate to **`http://127.0.0.1:8000/docs`** in your browser to test endpoints interactively.

### Example cURL Commands

```bash
# Create a task
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Buy milk\"}"

# Fetch all tasks
curl -X GET http://127.0.0.1:8000/tasks

# Update a task
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d "{\"done\": true}"

# Delete a task
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

---

## 💡 Architecture & Key Concepts Applied

- **Separation of Concerns**: Endpoint handlers (`main.py`), Pydantic data schemas (`models.py`), and storage operations (`database.py`) are strictly decoupled.
- **REST Principles**: Endpoints map to noun resources (`/tasks`), using proper HTTP verbs and standard HTTP status codes.
- **Pydantic Validation**: Automatic parsing and custom field validators for string trimming and empty field checks.
- **Type Safety**: Python type annotations on all parameters and returns ensure high code clarity and maintainability.

---

## 📄 License

Distributed under the MIT License. Built for FlyRank Backend Track.
