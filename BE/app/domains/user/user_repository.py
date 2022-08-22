from abc import ABC, abstractmethod
from typing import List, Optional

from BE.app.domains.user import User


class UserRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""

    @abstractmethod
    def create(self, book: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, book: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError
