from abc import ABC
from abc import abstractmethod

from ch_02.model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        pass

    @abstractmethod
    def get(self, reference) -> Batch:
        pass
