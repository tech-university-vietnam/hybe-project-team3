from datetime import datetime, timedelta
from typing import Optional
import jwt

from app.domains.user.user_repository import UserRepository
from app.config import get_settings
from fastapi import HTTPException, status


class JWTService:
    config = get_settings()

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def encode(self, user_id: str) -> str:
        payload = {'exp': datetime.utcnow() + timedelta(days=7),
                   'iat': datetime.utcnow(),
                   'sub': user_id}
        return jwt.encode(payload,
                          self.config.SECRET,
                          algorithm="HS256")

    def validate_token(self, auth: str) -> Optional[str]:
        """
        Decode JWT token to get use_id => return user_id
        """
        try:
            token = str.replace(str(auth), 'Bearer ', '')
            payload = jwt.decode(
                token,
                self.config.SECRET, algorithms=["HS256"])
            user_id = payload.get('sub')
            if (self.user_repo.check_token(
                    user_id,
                    token=token)):
                return user_id
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="token is invalid")
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
