from typing import Optional
from datetime import datetime


class Auth:

    def __init__(self, username, email, hash_password, salt):
        self.username: str = username
        self.email: str = email
        self.hash_password: str = hash_password
        self.salt: str = salt
