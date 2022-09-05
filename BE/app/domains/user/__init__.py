from app import register_class
from .user_repository import UserRepository
from .user_service import UserService

register_class(UserRepository)
register_class(UserService)
