from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    """
    Represents a complete Task resource stored in the system.
    """
    id: int = Field(..., description="Unique auto-generated task identifier")
    title: str = Field(..., description="Title or description of the task")
    done: bool = Field(False, description="Completion status of the task")


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    Requires a non-empty title. 'id' and 'done' are set automatically by the server.
    """
    title: str = Field(..., description="Title of the task")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """
        Validates that the title is not empty or whitespace-only.
        """
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty")
        return trimmed


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    All fields are optional; clients can update 'title', 'done', or both.
    """
    title: Optional[str] = Field(None, description="Updated title of the task")
    done: Optional[bool] = Field(None, description="Updated completion status")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        """
        If title is provided in update payload, ensure it is not empty or whitespace-only.
        """
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Title must be a string")
            trimmed = value.strip()
            if not trimmed:
                raise ValueError("Title cannot be empty")
            return trimmed
        return value
