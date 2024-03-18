from collections.abc import Iterable

from fastapi import APIRouter
from fastapi import FastAPI

from infrastructure.adapters.orm import start_mappers
from .views import router as batch_router


def create(routers: Iterable[APIRouter]) -> FastAPI:
    """FastAPI application factory."""

    application = FastAPI()

    for router in routers:
        application.include_router(router)

    start_mappers()

    return application


app = create([batch_router])
