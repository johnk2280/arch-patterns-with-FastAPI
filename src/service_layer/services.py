from collections.abc import Sequence
from datetime import datetime
from typing import Any
from typing import Protocol

from domain import allocate
from domain import Batch
from domain import OrderLine
from service_layer.exceptions import InvalidSkuError
from service_layer.ports import AbstractRepository
from service_layer.ports import AbstractUOW


def is_valid_sku(sku: str, batches: Sequence[Batch]) -> bool:
    return sku in {b.sku for b in batches}


class CommitterProtocol(Protocol):
    async def commit(self) -> None:
        ...


async def allocate_line(
    line: OrderLine,
    repo: AbstractRepository[Batch],
    session: CommitterProtocol,
) -> Batch:
    batches = await repo.get_many()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSkuError(str(line.sku)) from None

    batch = allocate(line, batches)
    await session.commit()
    return batch


async def add_batch(
    batch_data: dict[str, Any],
    uow: AbstractUOW,
) -> Batch:
    async with uow:
        batch = await uow.batches.add(batch_data)
        await uow.commit()

    return batch
