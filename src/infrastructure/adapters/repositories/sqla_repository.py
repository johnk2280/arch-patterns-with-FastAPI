from typing import Any
from typing import Generic
from typing import TypeVar

from service_layer.ports import AbstractRepository

M = TypeVar("M", bound=AbstractRepository)

class SQLARepository(AbstractRepository, Generic[M]):



    def _create(self, *args, **kwargs) -> Any:
        pass

    def _read(self, *args, **kwargs) -> Any:
        pass

    def _update(self, *args, **kwargs) -> Any:
        pass

    def _delete(self, *args, **kwargs) -> Any:
        pass