from pydantic import BaseModel


class GreetingSchema(BaseModel):
    name: str
