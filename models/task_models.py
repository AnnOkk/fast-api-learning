import uuid

from pydantic import BaseModel

class Task(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    is_completed: bool = False

class TaskDTO(BaseModel):
    title: str
    description: str | None = None