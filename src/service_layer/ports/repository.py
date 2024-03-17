from abc import ABC
from abc import abstractmethod
from typing import Any


class AbstractRepository(ABC):

    @abstractmethod
    def _create(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _read(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _update(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _delete(self, *args, **kwargs) -> Any:
        pass

    def get(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def add(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def list(self) -> Any:
        raise NotImplementedError
