from pydantic import BaseModel


class HospitalItem(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SeedResponse(BaseModel):
    msg: str
