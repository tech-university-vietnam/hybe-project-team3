import jwt
from app.main import get_settings, reusable_oauth2
from fastapi import Depends


class JWTService:
    def __init__(self) -> None:
        self.config = get_settings()

    def encode(self, user_id: str) -> str:
        payload = {'user_id': user_id}
        return jwt.encode(payload,
                          self.config.SECRET,
                          algorithm="HS256")

    def validate_token(self, http_authorization_credentials=Depends(
                       reusable_oauth2)) -> str:
        """
        Decode JWT token to get username => return username
        """
        payload = jwt.decode(http_authorization_credentials.credentials,
                             self.config.SECRET, algorithms=["HS256"])
        return payload.get("user_id")
