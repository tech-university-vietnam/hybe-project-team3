from pydantic import BaseModel


class CommonResponse(BaseModel):
    msg: str
