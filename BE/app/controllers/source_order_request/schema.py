from pydantic import BaseModel


class SourceOrderCreate(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SeedResponse(BaseModel):
    msg: str