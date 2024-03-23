from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence
from typing import Any
from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):

    async def add(self, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    async def _create(self, *args: Any, **kwargs: Any) -> Any:
        pass

    async def get(self, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError

    async def get_many(self, *args: Any, **kwargs: Any) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def _read(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def _update(self, *args: Any, **kwargs: Any) -> T:
        pass

    @abstractmethod
    async def _delete(self, *args: Any, **kwargs: Any) -> Any:
        pass
