from fastapi import Depends

from app.utils.unitofwork import IUnitOfWork, UnitOfWork
from app.services.todo_service import ToDoService


async def get_todo_service(uow: IUnitOfWork = Depends(UnitOfWork)):
    return ToDoService(uow)