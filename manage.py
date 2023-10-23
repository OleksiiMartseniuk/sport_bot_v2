import logging
import asyncio
from src.services.import_data import ImportDataService
from src.services.profile import ProfileService
from src.services.history import HistoryService
from src.utils.unitofwork import SqlAlchemyUnitOfWork
from src.settings import BASE_DIR

from src.bot.main import main as bot

# https://github.com/artemonsh/fastapi-onion-architecture/blob/pt2_unit_of_work/src/utils/unitofwork.py
# async def main():
#     i = ImportDataService()
#     uow = i.uow
#     async with uow:
#         # Программа на турнике для набора массы
#         # await uow.program.update(data={"title": "Программа на турнике для набора массы"}, id=1)
#         # await uow.commit()
#         a = await uow.exercise.all(limit=5, offset=5)
#         # c = await uow.exercise.all(offset=1, limit=2, count=True, number_of_approaches=4)
#         # print(c)
#         print(a[0].title)
        # a = await uow.exercise.exists(program_id=2)
        # d = await uow.category.get(id=1)
        # a = await uow.history_exercise.get(o=123)
        # print(d)
        # await uow.user.update(data={"program_id": 1}, id=1)
    #     # e = await uow.exercise.update(id=1, data={"title": "Подтягивания широким хватом"})
    #     await uow.commit()
    #     # print(e)
    # await ImportDataService().import_file(path=(BASE_DIR / "tmp/import_data.csv"))
    # uow = SqlAlchemyUnitOfWork()
    # profile_service = ProfileService(uow=uow, id=1)
    # # await profile_service.subscribe_to_program(program_id=13)
    # await profile_service.unsubscribe_to_program()
    # h = HistoryService(uow)
    # await h.create_history_exercise(1, 1, 1, 4, 5)

# asyncio.run(main())
# Add log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
asyncio.run(bot())


