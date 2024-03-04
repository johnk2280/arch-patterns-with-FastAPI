from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

M = TypeVar('M')
S = TypeVar('S', bound=Session)
AS = TypeVar('AS', bound=AsyncSession)


class AbstractRepository(ABC, Generic[M, S]):

    model_class: type[M]

    def __init__(self, session: S) -> None:
        if not self.model_class:
            raise ValueError(
                'Can not initiate the class without model_class attribute',
            )

        self.session = session

    @abstractmethod
    def add(self, item: M) -> None:
        pass

    @abstractmethod
    def get(self, reference: str) -> M:
        pass

    @abstractmethod
    def list(self) -> list[M]:
        pass


class AbstractAsyncRepository(ABC, Generic[M, AS]):

    model_class: type[M]

    def __init__(self, session: AS) -> None:
        if not self.model_class:
            raise ValueError(
                'Can not initiate the class without model_class attribute',
            )

        self.session = session

    @abstractmethod
    async def add(self, item: M) -> None:
        pass

    @abstractmethod
    async def get(self, reference: str) -> M:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[M]:
        pass
