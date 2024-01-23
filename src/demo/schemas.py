from pydantic import BaseModel


class GreetingSchema(BaseModel):
    name: str


class AccountSerializer(BaseModel):
    id: int
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    avatar: str | None

    class Config:
        orm_mode = True
