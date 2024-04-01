from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_api_add_batch(
    async_session: AsyncSession,
    async_client: AsyncClient,
):
    pass