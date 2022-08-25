from typing import Optional

from app.model.auth import Auth
from app.infrastructure.postgresql.database import session
from app.infrastructure.postgresql.user.user_dto import UserDTO


class AuthRepository:
    """User Repository defines a repository interface for user entity."""

    def query_auth_user(self, email: str) -> Optional[Auth]:
        # Query from database here
        auth_user = session.query(UserDTO).filter(
            (UserDTO.email == email)).first()
        if auth_user:
            return Auth(auth_user.id, auth_user.username, auth_user.email,
                        auth_user.hash_pw)
        else:
            return None
