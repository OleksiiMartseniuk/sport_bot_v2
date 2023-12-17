from fastapi.requests import Request

from sqladmin.authentication import AuthenticationBackend

from src.services.hash import Hasher
from src.settings import SECRET_KEY
from src.utils.unitofwork import SqlAlchemyUnitOfWork


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        self.uow = SqlAlchemyUnitOfWork()
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        async with self.uow:
            user = await self.uow.user.get_or_none(username=username)
            if user and user.is_staff:
                is_hash_password = Hasher.verify_password(
                    plain_password=password,
                    hashed_password=user.password,
                )
                if is_hash_password is False:
                    return False
            else:
                return False
            token = await self.uow.token.get_or_create(user_id=user.id)
            await self.uow.commit()
            request.session.update({"token": token.token})
        return True

    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        if token:
            async with self.uow:
                await self.uow.token.delete(token=token)
                await self.uow.commit()
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        async with self.uow:
            token = await self.uow.token.get_or_none(token=token)
            if token is None:
                return False
        return True


authentication_backend = AdminAuth(secret_key=SECRET_KEY)
