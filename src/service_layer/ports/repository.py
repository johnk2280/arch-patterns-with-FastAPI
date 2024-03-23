from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence
from typing import Any
from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):

    def add(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def _create(self, *args, **kwargs) -> T:
        pass

    def get(self, *args, **kwargs) -> T:
        raise NotImplementedError

    def get_many(self, *args, **kwargs) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    def _read(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _update(self, *args, **kwargs) -> T:
        pass

    @abstractmethod
    def _delete(self, *args, **kwargs) -> Any:
        pass
