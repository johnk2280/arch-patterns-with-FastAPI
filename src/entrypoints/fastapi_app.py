from collections.abc import Iterable

from fastapi import APIRouter
from fastapi import FastAPI

from infrastructure.rest_api import batch_router


def create(routers: Iterable[APIRouter]) -> FastAPI:
    """FastAPI application factory."""
    application = FastAPI()

    for router in routers:
        application.include_router(router)

    return application


app = create([batch_router])
