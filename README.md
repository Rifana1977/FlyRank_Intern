# Task Management REST API (FastAPI)

A clean, production-ready, beginner-friendly Task Management REST API built with **Python 3.10+** and **FastAPI** using an **in-memory list** data store. Designed for the **FlyRank Backend Track (Week 2)** assignment.

---

## 🚀 Features

- **FastAPI Framework**: Blazing-fast performance, automatic request validation, and OpenAPI schema generation.
- **RESTful API Principles**: Proper use of standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) and appropriate status codes (`200`, `201`, `204`, `400`, `404`).
- **Interactive OpenAPI Documentation**: Built-in Swagger UI available at `/docs`.
- **In-Memory Storage**: Fast, lightweight Python list database with auto-incrementing IDs.
- **Input Validation**: Strict request payload validation using Pydantic models (empty or whitespace-only titles are rejected with `400 Bad Request`).
- **Type Hinting**: Clean, fully typed Python code throughout models, storage, and endpoint handlers.

---

## 📁 Project Structure

```
FlyRank_Intern/
├── app/
│   ├── __init__.py       # Package initializer
│   ├── main.py          # FastAPI application & REST endpoint routes
│   ├── models.py        # Pydantic schemas & payload validators
│   └── database.py      # In-memory list store & data access operations
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

### 4. Run the Development Server
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## 📚 API Endpoints & Reference

Interactive Swagger UI documentation is live at **`http://127.0.0.1:8000/docs`**.

| Method | Endpoint | Description | Status Code | Error Status |
|---|---|---|---|---|
| `GET` | `/` | API Metadata & Endpoint list | `200 OK` | N/A |
| `GET` | `/health` | Health Check | `200 OK` | N/A |
| `GET` | `/tasks` | List all tasks | `200 OK` | N/A |
| `GET` | `/tasks/{id}` | Get task by ID | `200 OK` | `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `201 Created` | `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title/status | `200 OK` | `400 Bad Request` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `204 No Content` | `404 Not Found` |

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

#### 3. Create Task (`POST /tasks`)
- **Request Body**:
```json
{
  "title": "Buy milk"
}
```
- **Response `201 Created`**:
```json
{
  "id": 1,
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

#### 4. Get Task by ID (`GET /tasks/1`)
- **Response `200 OK`**:
```json
{
  "id": 1,
  "title": "Buy milk",
  "done": false
}
```
- **Task Not Found -> `404 Not Found`**:
```json
{
  "error": "Task not found"
}
```

#### 5. Update Task (`PUT /tasks/1`)
- **Request Body**:
```json
{
  "title": "Buy organic milk",
  "done": true
}
```
- **Response `200 OK`**:
```json
{
  "id": 1,
  "title": "Buy organic milk",
  "done": true
}
```

#### 6. Delete Task (`DELETE /tasks/1`)
- **Response `204 No Content`** *(Empty body)*

---

## 🧪 Testing with cURL / Postman / Swagger UI

### Using Interactive Swagger UI
Navigate to `http://127.0.0.1:8000/docs` in your browser to test endpoints interactively.

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
