from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.schemas.schema_todo import ToDoDelete, ToDoFromDB, ToDoCreate
from app.services.todo_service import ToDoService
from app.api.dependencies import get_todo_service


todo_router = APIRouter(prefix="/todo", tags=["ToDo"])
templates = Jinja2Templates(directory="app/api/templates")


@todo_router.post("/todos/")
async def create_todo(
    todo_data: ToDoCreate,
    todo_service: ToDoService = Depends(get_todo_service),
):
    task_id = await todo_service.add_todo(todo_data)
    return task_id


@todo_router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int, todo_service: ToDoService = Depends(get_todo_service)
):
    todo_id = ToDoDelete(id=todo_id)
    task_id = await todo_service.delete_todo(todo_id)

    if task_id is None:
        return []

    return task_id


@todo_router.get("/todos/", response_model=List[ToDoFromDB])
async def get_todos(todo_service: ToDoService = Depends(get_todo_service)):
    return await todo_service.get_todos()


@todo_router.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )
