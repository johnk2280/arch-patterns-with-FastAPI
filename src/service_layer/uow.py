from typing import Any

from service_layer.ports import AbstractUOW


class BatchUOW(AbstractUOW):
    async def __aenter__(self) -> Any:
        pass

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
