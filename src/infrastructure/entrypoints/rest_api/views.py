from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import Batch
from infrastructure.adapters.orm import batches
from infrastructure.adapters.orm import get_async_session
from infrastructure.adapters.repositories import AsyncBatchRepository
from infrastructure.entrypoints.rest_api.schema import OrderLineCreateSchema

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Batchg)
    result = await session.execute(stmt)
    return result.mappings().all()


@router.post('/allocate')
async def allocate(
    order_line: OrderLineCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    # repo: AsyncBatchRepository = Depends(),
):
    repo = AsyncBatchRepository(session)
    # sqlalchemy.exc.ArgumentError: Column expression,
    # FROM clause, or other columns clause element expected,
    # got <class 'domain.model.Batch'>.
    # TODO: при старте приложения не запущен маппер моделей и таблиц.
    #  Если его запусти в фабрике приложения, то ошибка исчезнет.
    batches = await repo.get_all()
    return batches
