import json

from fastapi import Body
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response

from demo.schemas import GreetingSchema

app = FastAPI()


@app.get('/')
def root():
    return 'Hello World'


# Передача через url
@app.get('/greet/{name}')
def greet_1(name: str):
    return Response(f'Hello {name}')


# Передача через query params в query string
@app.get('/greet')
def greet_2(name: str = 'World'):
    return Response(f'Hello {name}')


# Доступ к объекту Request
@app.post('/greet_0')
def greet_3(request: Request, name: str = Body(...), ):
    return Response(f'Hello {name}. Request: {request}')


# Десериализация (и очевидно валидация) входных данных,
# поступающих в теле запроса в качестве JSON.
@app.post('/greet')
def greet_3(schema: GreetingSchema):
    return Response(f'Hello {schema.name}')
