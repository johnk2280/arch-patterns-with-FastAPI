from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from domain.exeptions import OutOfStockError
from service_layer.exceptions import InvalidSkuError


async def handle_no_result_found(
    _: Request,
    exc: OutOfStockError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        content={
            'message': str(exc),
        },
    )


async def handle_invalid_sku(
    _: Request,
    exc: InvalidSkuError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'message': f'Недопустимый артикул: {str(exc)}',
        }
    )
