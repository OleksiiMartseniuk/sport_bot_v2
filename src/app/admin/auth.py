from fastapi.requests import Request

from sqladmin.authentication import AuthenticationBackend

from src.services.hash import Hasher
from src.settings import SECRET_KEY


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        uow = request.state.uow
        user = await uow.user.get_or_none(username=username)
        if user and user.is_staff:
            is_hash_password = Hasher.verify_password(
                plain_password=password,
                hashed_password=user.password,
            )
            if is_hash_password is False:
                return False
        else:
            return False
        token = await uow.token.get_or_create(user_id=user.id)
        await uow.commit()
        request.session.update({"token": token.token})
        return True

    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        if token:
            await request.state.uow.token.delete(token=token)
            await request.state.uow.commit()
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        token = await request.state.uow.token.get_or_none(token=token)
        if token is None:
            return False
        return True


authentication_backend = AdminAuth(secret_key=SECRET_KEY)
