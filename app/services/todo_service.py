from app.api.schemas.schema_todo import IdFromDB, ToDoFromDB
from app.utils.unitofwork import IUnitOfWork


class ToDoService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_todo(self, data):
        todo_dict = data.model_dump()

        async with self.uow:
            model_from_db = await self.uow.todo.add_one(todo_dict)
            id_to_return = IdFromDB.model_validate(model_from_db)
            await self.uow.commit()
            return id_to_return

    async def delete_todo(self, data):
        todo_dict = data.model_dump()

        async with self.uow:
            model_from_db = await self.uow.todo.delete_one(todo_dict)

            if model_from_db is None:
                return None

            id_to_return = IdFromDB.model_validate(model_from_db)
            await self.uow.commit()
            return id_to_return

    async def get_todos(self):
        async with self.uow:
            todos = await self.uow.todo.find_all()
            return [ToDoFromDB.model_validate(todo) for todo in todos]
