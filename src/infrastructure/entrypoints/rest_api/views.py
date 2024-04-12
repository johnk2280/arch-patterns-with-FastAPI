from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain import OrderLine
from domain.models import Batch
from infrastructure.storage.orm import get_async_session
from service_layer.services import add_batch
from service_layer.services import allocate_line
from service_layer.uow import BatchUOW
from .schema import BatchCreateSchema
from .schema import BatchSchema
from .schema import OrderLineCreateSchema

router = APIRouter(prefix='', tags=['batches'])


@router.get(
    '/batches',
    status_code=status.HTTP_200_OK,
    response_model=BatchSchema,
)
async def get_batches(
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Batch]:
    return (await session.execute(select(Batch))).scalars().all()


@router.post(
    '/batches',
    status_code=status.HTTP_201_CREATED,
    response_model=BatchSchema,
)
async def create_batches(
    batch: BatchCreateSchema,
) -> Batch:
    uow = BatchUOW()
    return await add_batch(
        {
            'reference': batch.reference,
            'sku': batch.sku,
            '_purchased_quantity': batch.purchased_quantity,
            'eta': batch.eta,
        },
        uow
    )


@router.post(
    '/allocate',
    status_code=status.HTTP_201_CREATED,
    response_model=BatchSchema,
)
async def allocate_order_line(order_line: OrderLineCreateSchema) -> Batch:
    uow = BatchUOW()
    return await allocate_line(
        OrderLine(**order_line.model_dump()),
        uow
    )
