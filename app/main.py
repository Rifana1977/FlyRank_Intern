from typing import List, Any
from fastapi import FastAPI, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.models import Task, TaskCreate, TaskUpdate
from app.database import db
from app.routers import auth as auth_router

app = FastAPI(
    title="Task Management API",
    description="A simple in-memory Task Management REST API built with FastAPI for FlyRank Week 2",
    version="1.0"
)

# Register routers
app.include_router(auth_router.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Custom exception handler to catch validation errors and return HTTP 400 with requirement-matching error JSON.
    """
    for err in exc.errors():
        msg = err.get("msg", "")
        loc = err.get("loc", ())
        if "Title cannot be empty" in msg or "title" in loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Title cannot be empty"}
            )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid input"}
    )


@app.get("/", status_code=status.HTTP_200_OK)
def get_root() -> dict:
    """
    GET / - Returns API name, version, and available endpoints list.
    """
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", status_code=status.HTTP_200_OK)
def get_health() -> dict:
    """
    GET /health - Health check endpoint to monitor API status.
    """
    return {
        "status": "ok"
    }


@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def get_all_tasks() -> List[Task]:
    """
    GET /tasks - Retrieves all tasks stored in memory.
    """
    return db.get_all()


@app.get("/tasks/{id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task_by_id(id: int) -> Any:
    """
    GET /tasks/{id} - Retrieves a single task by path parameter 'id'.
    Returns 404 {"error": "Task not found"} if the task does not exist.
    """
    task = db.get_by_id(id)
    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate) -> Any:
    """
    POST /tasks - Creates a new task.
    Accepts: {"title": "Buy milk"}
    Auto-generates 'id' and sets 'done' = false.
    Returns: 201 Created with the new task object.
    Missing or empty title returns: 400 Bad Request {"error": "Title cannot be empty"}.
    """
    new_task = db.create(task_in)
    return new_task


@app.put("/tasks/{id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(id: int, task_in: TaskUpdate) -> Any:
    """
    PUT /tasks/{id} - Updates title and/or done status of an existing task.
    Returns updated task.
    Returns 404 {"error": "Task not found"} if task doesn't exist.
    Returns 400 {"error": "Invalid input"} for invalid payload or empty title.
    """
    task = db.get_by_id(id)
    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )

    if task_in.title is None and task_in.done is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid input"}
        )

    updated_task = db.update(id, task_in)
    return updated_task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int) -> Response:
    """
    DELETE /tasks/{id} - Deletes a task by ID.
    Returns 204 No Content on success (no body returned).
    Returns 404 {"error": "Task not found"} if task doesn't exist.
    """
    success = db.delete(id)
    if not success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


