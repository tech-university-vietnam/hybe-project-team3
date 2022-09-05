from app.services.jwt_service import JWTService
from app import register_class
from app.services.auth_service import AuthService

register_class(AuthService)
register_class(JWTService)