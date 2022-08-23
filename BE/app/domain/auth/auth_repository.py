from typing import Optional

from app.model.auth import Auth


class AuthRepository:
    """User Repository defines a repository interface for user entity."""

    def query_auth_user(self, username: str, email: str) -> Optional[Auth]:
        # Query from database here
        mock_auth_user = Auth('bao_nguyen', 'bao_nguyen@mckinsey.com', 'hash', 'salt')
        return mock_auth_user
