from collections.abc import Iterable

from fastapi import APIRouter
from fastapi import FastAPI

from domain.exeptions import OutOfStockError
from infrastructure.storage.orm import start_mappers
from .error_handlers import handle_no_result_found
from .views import router as batch_router


def create(routers: Iterable[APIRouter]) -> FastAPI:
    """FastAPI application factory."""

    application = FastAPI()

    for router in routers:
        application.include_router(router)

    application.exception_handler(OutOfStockError)(handle_no_result_found)

    start_mappers()

    return application


app = create([batch_router])
