from app.model.user import User


class Auth:
    def __init__(self, id, email, hash_pw, token):
        self.id: int = id
        self.email: str = email
        self.hash_pw: str = hash_pw
        self.token: str = token

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            email=user.email,
            hash_pw=user.hash_pw,
            token=user.token)
