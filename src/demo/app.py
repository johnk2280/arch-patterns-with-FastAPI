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
def greet_2(name: str | None = None):
    return Response(f'Hello {name}')
