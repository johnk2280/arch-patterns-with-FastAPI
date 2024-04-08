from typing import Any

from infrastructure.storage.orm.database import async_session_maker
from infrastructure.storage.repositories import AsyncBatchRepo
from service_layer.ports import AbstractUOW


class BatchUOW(AbstractUOW):
    def __init__(self) -> None:
        self._session_factory = async_session_maker

    async def __aenter__(self) -> Any:
        self._session = self._session_factory()

        self.batches = AsyncBatchRepo(self._session)

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
