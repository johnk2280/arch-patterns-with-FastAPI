from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from domain.model import Batch
from infrastructure.adapters.orm import Batch
from infrastructure.adapters.orm import get_async_session

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Batch)
    result = await session.execute(stmt)
    return result.mappings().all()

