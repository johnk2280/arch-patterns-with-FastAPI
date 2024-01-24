from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from demo.config import settings
from .accounts import api as accounts_api

app = FastAPI()
app.mount(
    settings.STATIC_URL,
    StaticFiles(directory=settings.STATIC_DIR),
    name='static'
)

accounts_api.initialize_app(app)
