from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):

    def add(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _create(self, *args, **kwargs) -> Any:
        pass

    def get(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def get_many(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _read(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _update(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _delete(self, *args, **kwargs) -> Any:
        pass
