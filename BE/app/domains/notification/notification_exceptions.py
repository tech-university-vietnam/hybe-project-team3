class RequestNotExistError(Exception):
    message = "Request is not exist"

    def __str__(self):
        return RequestNotExistError.message