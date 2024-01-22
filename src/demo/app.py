from fastapi import FastAPI
from fastapi import Response

app = FastAPI()


@app.get('/')
def root():
    return 'Hello World'


@app.get('/example')
def root():
    return Response('Hello World')
