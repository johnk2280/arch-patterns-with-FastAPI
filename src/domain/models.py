import datetime
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .exeptions import OutOfStockError


class DomainModel:
    pass


@dataclass(unsafe_hash=True)
class OrderLine(DomainModel):
    order_id: str
    sku: str
    qty: int
    id: int | None = None

    def __repr__(self) -> str:
        return (f'OrderLine('
                f'order_id={self.order_id}, '
                f'sku={self.sku}, '
                f'qty={self.qty}, '
                f'id={self.id})')

    def __str__(self) -> str:
        return (f'OrderLine('
                f'order_id={self.order_id}, '
                f'sku={self.sku}, '
                f'qty={self.qty}, '
                f'id={self.id})')


class Batch(DomainModel):
    _allocations: set[OrderLine]

    def __init__(
        self,
        reference: str,
        sku: str,
        _purchased_quantity: int,
        eta: datetime.date | None = None,
        id_: int | None = None,
    ) -> None:
        self.id = id_
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = _purchased_quantity
        self._allocations = set[OrderLine]()

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}('
                f'ref={self.reference!r},'
                f' sku={self.sku!r},'
                f' eta={self.eta!r}'
                f')')

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Batch):
            return self.reference == other.reference

        return False

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: 'Batch') -> bool:
        if self.eta is None:
            return False

        if other.eta is None:
            return True

        return self.eta > other.eta

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


class Product(DomainModel):

    def __int__(self, sku: str, batches: list[Batch], version: int) -> None:
        self.sku = sku
        self.batches = batches
        self.version = version

    def allocate(self, line: OrderLine) -> Batch:
        try:
            batch = next(
                batch for batch in sorted(self.batches)
                if batch.can_allocate(line)
            )
            batch.allocate(line)
            return batch
        except StopIteration:
            raise OutOfStockError(f'Артикула {line.sku} нет в наличии')


def make_batch_and_line(
    sku: str,
    batch_qty: int,
    line_qty: int,
) -> tuple[Batch, OrderLine]:

    return (
        Batch('batch-001', sku, batch_qty, eta=datetime.date.today()),
        OrderLine('order-123', sku, line_qty),
    )


# Служба модели предметной области (бизнес-процесс)
def allocate(line: OrderLine, batches: Sequence[Batch]) -> Batch:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line),
        )

        batch.allocate(line)

        return batch
    except StopIteration:
        raise OutOfStockError(f'Артикула {line.sku} нет в наличии')
