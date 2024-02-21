from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.adapters.orm import batches
from infrastructure.adapters.orm import get_async_session

router = APIRouter(prefix='', tags=['batches'])


@router.get('/batches')
async def get_batches(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(batches)
    result = await session.execute(stmt)
    return result.mappings().all()

