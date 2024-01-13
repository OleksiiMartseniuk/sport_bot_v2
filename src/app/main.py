from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from sqladmin import Admin

from src.database.base import engine_async
from src.app.admin.models import admin_view_models
from src.app.admin.auth import authentication_backend
from src.settings import CORS_ORIGINS


app = FastAPI()
admin = Admin(
    app=app,
    engine=engine_async,
    authentication_backend=authentication_backend,
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=[
#         "Content-Type",
#         "Set-Cookie",
#         "Access-Control-Allow-Headers",
#         "Access-Control-Allow-Origin",
#         "Authorization",
#         "X-Forwarded-For",
#     ],
# )


@app.get("/")
async def redirect_admin():
    return RedirectResponse(url="/admin")


for admin_view in admin_view_models:
    admin.add_view(admin_view)
