from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain import OrderLine
from domain.models import Batch
from infrastructure.storage.orm import get_async_session
from infrastructure.storage.repositories import AsyncBatchRepo
from service_layer.services import allocate_line
from .schema import BatchSchema
from .schema import OrderLineCreateSchema

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches(
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(Batch))
    return result.mappings().all()


@router.post(
    '/allocate',
    status_code=status.HTTP_201_CREATED,
    response_model=BatchSchema,
)
async def allocate_order_line(
    order_line: OrderLineCreateSchema,
    async_session: AsyncSession = Depends(get_async_session)
) -> Batch:
    repo = AsyncBatchRepo(async_session)
    return await allocate_line(
        OrderLine(**order_line.model_dump()),
        repo,
        async_session,
    )
