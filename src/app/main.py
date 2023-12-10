import contextlib
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from sqladmin import Admin

from src.database.base import engine_async
from src.app.admin.models import admin_view_models
from src.app.admin.auth import authentication_backend
from src.utils.unitofwork import SqlAlchemyUnitOfWork


class State(TypedDict):
    uow: SqlAlchemyUnitOfWork


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    uow = SqlAlchemyUnitOfWork()
    async with uow:
        yield State(uow=uow)


app = FastAPI(lifespan=lifespan)
admin = Admin(
    app=app,
    engine=engine_async,
    authentication_backend=authentication_backend,
)


@app.get("/")
async def redirect_admin():
    return RedirectResponse(url="/admin")


for admin_view in admin_view_models:
    admin.add_view(admin_view)
