from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import Batch
from infrastructure.adapters.orm import get_async_session
from infrastructure.adapters.repositories import AsyncBatchRepository
from infrastructure.entrypoints.rest_api.schema import OrderLineCreateSchema

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Batch)
    result = await session.execute(stmt)
    return result.mappings().all()


@router.post('/allocate')
async def allocate(
    order_line: OrderLineCreateSchema,
    repo: AsyncBatchRepository = Depends(),
):
    batches = await repo.get_all()
    return batches
