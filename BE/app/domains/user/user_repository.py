from abc import ABC, abstractmethod
from typing import List, Optional

from BE.app.domains.user import User


class UserRepository(ABC):
    """User Repository defines a repository interface for user entity."""

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError
