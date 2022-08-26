from datetime import datetime, timedelta
from typing import Optional
import jwt
import datetime

from app.domain.user.user_repository import UserRepository
from app.config import get_settings, reusable_oauth2
from fastapi import Depends, HTTPException, status


class JWTService:
    config = get_settings()
    user_repo = UserRepository()

    def encode(self, user_id: str) -> str:
        payload = {'exp': datetime.utcnow() + timedelta(days=7),
                   'iat': datetime.utcnow(),
                   'sub': user_id}
        return jwt.encode(payload,
                          self.config.SECRET,
                          algorithm="HS256")

    def validate_token(self, http_authorization_credentials=Depends(
                       reusable_oauth2)) -> Optional[str]:
        """
        Decode JWT token to get use_id => return user_id
        """
        if http_authorization_credentials:
            try:
                payload = jwt.decode(
                    http_authorization_credentials.credentials,
                    self.config.SECRET, algorithms=["HS256"])
                user_id = payload.get('sub')
                if (self.user_repo.check_token(
                        user_id,
                        token=http_authorization_credentials.credentials)):
                    return user_id
            except (jwt.ExpiredSignatureError,
                    jwt.InvalidTokenError):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
