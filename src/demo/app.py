from fastapi import Body
from fastapi import FastAPI
from fastapi import Response

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


@app.post('/greet')
def greet_3(name: str = Body(...)):
    return Response(f'Hello {name}')