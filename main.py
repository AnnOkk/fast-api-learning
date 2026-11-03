import uuid

from fastapi import FastAPI, HTTPException

from models.task_models import TaskDTO, Task

app = FastAPI()

tasks_db = []

@app.post("/tasks")
def create_task(task_dto: TaskDTO):
    task = Task(title=task_dto.title, description=task_dto.description, id=uuid.uuid4())
    tasks_db.append(task)
    return task

@app.get("/tasks/{task_id}")
def get_task(task_id: uuid.UUID):
    task = find_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.get("/tasks")
def get_tasks(skip: int = 0, limit: int = 10):
    return tasks_db[skip:skip+limit]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: uuid.UUID):
    task = find_task_by_id(task_id)
    if task is  None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db.remove(task)
    return {"message": "Task deleted"}


@app.put("/tasks/{task_id}")
def update_task(task_id: uuid.UUID, task_dto: TaskDTO):
    task = find_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_dto.title
    task.description = task_dto.description
    task.is_completed = task_dto.is_completed
    return task


@app.get("/health")
async def health():
    return {"status": "ok"}


def find_task_by_id(task_id: uuid.UUID):
    for task in tasks_db:
        if task.id == task_id:
            return task
    return None