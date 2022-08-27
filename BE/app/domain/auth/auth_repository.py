from typing import Optional
from sqlalchemy.orm import Session
from app.model.auth import Auth
from app.infrastructure.postgresql.user.user_dto import UserDTO


class AuthRepository:
    """User Repository defines a repository interface for user entity."""

    def query_auth_user(self, email: str,
                        db: Session
                        ) -> Optional[Auth]:
        # Query from database here
        auth_user = db.query(UserDTO).filter(
            (UserDTO.email == email)).first()
        if auth_user:
            return Auth(auth_user.id, auth_user.email, auth_user.hash_pw,
                        auth_user.token)
        else:
            return None
