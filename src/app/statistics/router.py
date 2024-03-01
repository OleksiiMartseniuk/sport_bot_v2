from fastapi import APIRouter, Depends

from src.app.statistics.schemas import HistoryExercisesSchema
from src.app.utils import ResponseSchema, pagination
from src.utils.unitofwork import SqlAlchemyUnitOfWork, get_sql_alchemy_unit_of_work

router = APIRouter(prefix="/statistics")


@router.get("/list/{telegram_user_id}/")
async def get_statistics(
    telegram_user_id: int,
    pagination_params: dict[str, int] = Depends(pagination),
    uow: SqlAlchemyUnitOfWork = Depends(get_sql_alchemy_unit_of_work),
) -> ResponseSchema[HistoryExercisesSchema]:
    history_list = await uow.history_exercise.get_statistics(
        telegram_user_id=telegram_user_id, **pagination_params
    )
    history_count = await uow.history_exercise.count(telegram_user_id=telegram_user_id)
    history_list_data = [
        HistoryExercisesSchema.model_validate(h, from_attributes=True)
        for h in history_list
    ]
    return ResponseSchema[HistoryExercisesSchema](
        response=history_list_data,
        count=history_count,
    )
