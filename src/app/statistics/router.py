from fastapi import APIRouter, Depends

from src.app.statistics.schemas import HistoryExercisesSchema
from src.utils.unitofwork import SqlAlchemyUnitOfWork, get_sql_alchemy_unit_of_work

router = APIRouter(prefix="/statistics")


@router.get("/list/{telegram_user_id}/")
async def get_statistics(
    telegram_user_id: int,
    uow: SqlAlchemyUnitOfWork = Depends(get_sql_alchemy_unit_of_work),
) -> list[HistoryExercisesSchema]:
    history_list = await uow.history_exercise.get_statistics(
        telegram_user_id=telegram_user_id,
    )
    return [
        HistoryExercisesSchema.model_validate(h, from_attributes=True)
        for h in history_list
    ]
