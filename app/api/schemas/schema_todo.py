from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str


class ToDoDelete(BaseModel):
    id: int


class IdFromDB(ToDoDelete):
    class Config:
        from_attributes = True


class ToDoFromDB(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True