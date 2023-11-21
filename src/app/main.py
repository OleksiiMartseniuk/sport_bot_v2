import contextlib
from typing import AsyncIterator, TypedDict

from sqladmin import Admin
from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Route
from starlette.requests import Request

from src.database.base import engine
from src.app.admin.models import admin_view_models
from src.app.admin.auth import authentication_backend
from src.utils.unitofwork import SqlAlchemyUnitOfWork


class State(TypedDict):
    uow: SqlAlchemyUnitOfWork


async def redirect_admin(request: Request):
    return RedirectResponse(url="/admin")


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:
    uow = SqlAlchemyUnitOfWork()
    async with uow:
        yield {"uow": uow}


routes = [
    Route("/", endpoint=redirect_admin),
]

app = Starlette(lifespan=lifespan, routes=routes)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)


for admin_view in admin_view_models:
    admin.add_view(admin_view)
