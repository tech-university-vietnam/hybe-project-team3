

class Auth:
    def __init__(self, id, email, hash_pw, token):
        self.id: int = id
        self.email: str = email
        self.hash_pw: str = hash_pw
        self.token: str = token
