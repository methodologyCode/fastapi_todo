import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.endpoints.todo import todo_router


app = FastAPI()
app.include_router(todo_router)
path_to_static = os.path.join(os.path.dirname('./app/api/'), 'static')
app.mount("/static", StaticFiles(directory=path_to_static),
                  name="static")


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)