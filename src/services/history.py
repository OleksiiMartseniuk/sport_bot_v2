import logging

from src.utils.unitofwork import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


class HistoryService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow

    async def create_history_exercise(
        self,
        exercise_id: int,
        user_id: int,
        program_id: int,
        approach: int,
        number_of_repetitions: int,
        is_current_program: bool = True
    ) -> None:
        arguments = locals()
        del arguments["self"]
        del arguments["is_current_program"]

        if is_current_program:
            async with self.uow:
                is_program = await self.uow.user.exists(
                    id=user_id,
                    program_id=program_id,
                )
                if is_program is False:
                    raise ValueError(
                        f"User {user_id} is not subscribed to "
                        f"program {program_id}."
                    )
        async with self.uow:
            exercise = await self.uow.exercise.get(id=exercise_id)
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

            is_history_exercise = await self.uow.history_exercise.exists(
                **arguments
            )
            if is_history_exercise is True:
                raise ValueError(f"HistoryExercise is exists {arguments}.")

            await self.uow.history_exercise.create(data=arguments)
            await self.uow.commit()
