from src.database.models.user import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User]):
    model = User
