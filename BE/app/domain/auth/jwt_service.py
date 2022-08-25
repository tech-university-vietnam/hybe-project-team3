import jwt
from app.main import get_settings
import datetime


class JWTService:
    config = get_settings()

    @staticmethod
    def encode(user_id: str) -> str:

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload,
                          "hybe-secret",
                          algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(token, "hybe-secret")
            return payload
        except jwt.ExpiredSignatureError:
            return 'Expired token'
        except jwt.InvalidTokenError:
            return 'Wrong token'
