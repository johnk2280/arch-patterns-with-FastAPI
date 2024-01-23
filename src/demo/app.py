import json

from fastapi import Body
from fastapi import FastAPI
from fastapi import Form
from fastapi import Request
from fastapi import Response

from demo.schemas import GreetingSchema

app = FastAPI()


@app.post('/account')
def create_account(request: Request):
    ...


