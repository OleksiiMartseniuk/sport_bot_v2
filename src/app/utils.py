from typing import Generic, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ResponseSchema(BaseModel, Generic[T]):
    response: Union[list[T], T]
    count: int


def pagination(offset: int = 0, limit: int = 50) -> dict[str, int]:
    return {"offset": offset, "limit": limit}
