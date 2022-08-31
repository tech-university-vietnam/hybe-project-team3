from typing import Optional

from app.domains.helpers.database_repository import DatabaseRepository
from app.model.auth import Auth
from app.infrastructure.postgresql.user.user_dto import UserDTO


class AuthRepository:
    """User Repository defines a repository interface for user entity."""

    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = next(self.db_repo.get_db())

    def query_auth_user(self, email: str) -> Optional[Auth]:
        # Query from database here
        auth_user = self.db.query(UserDTO).filter(
            (UserDTO.email == email)).first()
        if auth_user:
            return Auth(auth_user.id, auth_user.email, auth_user.hash_pw,
                        auth_user.token)
        else:
            return None
