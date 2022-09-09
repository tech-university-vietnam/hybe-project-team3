class UserNotFoundError(Exception):
    message = "The user you spcecified does not exist."

    def __str__(self):
        return UserNotFoundError.message


class EmailAlreadyRegisteredError(Exception):
    message = "The email is already registered"

    def __str__(self):
        return EmailAlreadyRegisteredError.message


class EmailNotFoundError(Exception):
    message = "The email is not found"

    def __str__(self):
        return EmailNotFoundError.message