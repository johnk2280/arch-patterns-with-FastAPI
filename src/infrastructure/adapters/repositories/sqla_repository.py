from typing import Any
from typing import Generic
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from domain import Batch
from domain import DomainModel
from service_layer.ports import AbstractRepository

M = TypeVar("M", bound=DomainModel)


class AsyncSQLARepository(AbstractRepository, Generic[M]):

    model_class: type[M]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _create(self, *args, **kwargs) -> Any:
        pass

    async def _read(self, *args, **kwargs) -> Any:
        pass

    async def _update(self, *args, **kwargs) -> Any:
        pass

    async def _delete(self, *args, **kwargs) -> Any:
        pass


class AsyncBatchRepo(AsyncSQLARepository[Batch]):
    model_class = Batch
