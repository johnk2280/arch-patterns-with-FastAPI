from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import Batch
from infrastructure.orm.database import get_async_session

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches():
    session = next(get_async_session())
    stmt = select(Batch)
    result = await session.execute(stmt)
    return result.mappings().all()

