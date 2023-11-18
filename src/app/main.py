from sqladmin import Admin
from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Route
from starlette.requests import Request

from src.database.base import engine
from src.app.admin.models import admin_view_models
from src.app.admin.auth import authentication_backend


async def redirect_admin(request: Request):
    return RedirectResponse(url="/admin")


routes = [
    Route("/", endpoint=redirect_admin),
]

app = Starlette(routes=routes)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)


for admin_view in admin_view_models:
    admin.add_view(admin_view)


# https://aminalaee.dev/sqladmin/
# uvicorn src.app.main:app --reload
