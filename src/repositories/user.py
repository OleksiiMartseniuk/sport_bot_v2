from src.database.models.user import User
from src.utils.repository import SqlAlchemyRepository
from src.services.hash import Hasher


class UserRepository(SqlAlchemyRepository[User]):
    model = User

    async def create_staff(self, username: str, password: str) -> None:
        password_hash = Hasher.get_password_hash(password)
        await self.create(
            data={
                "username": username,
                "password": password_hash,
                "is_staff": True,
            }
        )

    async def create_superuser(self, username: str, password: str):
        password_hash = Hasher.get_password_hash(password)
        await self.create(
            data={
                "username": username,
                "password": password_hash,
                "is_staff": True,
                "is_superuser": True,
            }
        )
