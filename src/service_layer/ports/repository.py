from abc import ABC
from abc import abstractmethod
from typing import Any


class AbstractRepository(ABC):

    @abstractmethod
    def add(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def get(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def list(self) -> Any:
        pass
