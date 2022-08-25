import logging
import jwt
from app.main import get_settings


class JWTService:
    def __init__(self) -> None:
        self.config = get_settings()

    def encode(self, user_id: str) -> str:
        payload = {
                'user_id': user_id
            }
        return jwt.encode(
                payload,
                self.config.SECRET,
                algorithm="HS256")

    @staticmethod
    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.config.SECRET,
                                 algorithms=["HS256"])
            logging.info(payload)
            return payload
        except jwt.ExpiredSignatureError:
            return 'Expired token'
        except jwt.InvalidTokenError:
            return 'Wrong token'
