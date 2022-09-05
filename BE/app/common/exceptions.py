class DBError(Exception):
    message = "Error"

    def __str__(self):
        return DBError.message


class PermissionError(Exception):
    message = "Permission error"

    def __str__(self):
        return PermissionError.message
