import logging
from datetime import datetime

from src.utils.unitofwork import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


class HistoryService:
    @staticmethod
    async def create_history_exercise(
        uow_transaction: SqlAlchemyUnitOfWork,
        exercise_id: int,
        user_id: int,
        program_id: int,
        approach: int,
        number_of_repetitions: int,
        is_current_program: bool = True
    ) -> None:
        arguments = locals()
        del arguments["uow_transaction"]
        del arguments["is_current_program"]

        if is_current_program:
            is_program = await uow_transaction.user.exists(
                id=user_id,
                program_id=program_id,
            )
            if is_program is False:
                raise ValueError(
                    f"User {user_id} is not subscribed to "
                    f"program {program_id}."
                )
        exercise = await uow_transaction.exercise.get(id=exercise_id)
        if (
            number_of_repetitions < 0
            or approach <= 0
            or approach > exercise.number_of_approaches
        ):
            raise ValueError(
                f"Invalid value to fields [number_of_repetitions "
                f"{number_of_repetitions}, approach {approach}, "
                f"exercise.number_of_approaches "
                f"{exercise.number_of_approaches}]."
            )

        is_count = (
            await uow_transaction.history_exercise
            .get_count_history_today(**arguments)
        )
        if is_count:
            raise ValueError(f"HistoryExercise is exists {arguments}.")

        await uow_transaction.history_exercise.create(data=arguments)
        await uow_transaction.commit()
