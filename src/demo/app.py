from fastapi import FastAPI
from fastapi import Response

app = FastAPI()


@app.get('/')
def root():
    return 'Hello World'


@app.get('/greet')
def root(name: str):
    return Response(f'Hello {name}')
