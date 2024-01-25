from fastapi import UploadFile
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


# По сути deserializer
class AccountCreate(BaseModel):
    email: str
    username: str
    password: str


# По сути deserializer
class AccountUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    # avatar: UploadFile | None


