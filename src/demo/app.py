from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from demo.config import settings

app = FastAPI()
app.mount(
    settings.STATIC_URL,
    StaticFiles(directory=settings.STATIC_DIR),
    name='static'
)


