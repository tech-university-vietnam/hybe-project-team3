

class Auth:
    def __init__(self, id, username, email, hash_pw):
        self.id: int = id
        self.username: str = username
        self.email: str = email
        self.hash_pw: str = hash_pw
