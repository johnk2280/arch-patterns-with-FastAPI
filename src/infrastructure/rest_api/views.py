from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from domain.model import Batch
from domain.model import Batch
from infrastructure.adapters.orm import get_async_session

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches(
    session: AsyncSession = Depends(get_async_session),
):
    # TODO: sqlalchemy.exc.ArgumentError:
    #  Column expression, FROM clause, or other columns clause element
    #  expected, got <class 'domain.model.Batch'>.
    stmt = select(Batch)
    result = await session.execute(stmt)
    return result.mappings().all()

