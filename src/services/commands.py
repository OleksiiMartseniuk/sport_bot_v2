from src.utils.unitofwork import SqlAlchemyUnitOfWork


class Commands:
    @staticmethod
    async def create_user_staff(username: str, password: str) -> None:
        uow = SqlAlchemyUnitOfWork()
        async with uow:
            await uow.user.create_staff(username=username, password=password)
            await uow.commit()

    @staticmethod
    async def create_superuser(username: str, password: str) -> None:
        uow = SqlAlchemyUnitOfWork()
        async with uow:
            await uow.user.create_superuser(
                username=username,
                password=password,
            )
            await uow.commit()
