import datetime
from dataclasses import dataclass
from typing import Any


class OutOfStockError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


class Batch:
    def __init__(
        self,
        ref: str,
        sku: str,
        qty: int,
        eta: datetime.date | None = None
    ) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
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


def make_batch_and_line(
    sku: str,
    batch_qty: int,
    line_qty: int,
) -> tuple[Batch, OrderLine]:
    return (
        Batch('batch-001', sku, batch_qty, eta=datetime.date.today()),
        OrderLine('order-123', sku, line_qty)
    )


# Служба модели предметной области (бизнес-процесс)
def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStockError(f'Артикула {line.sku} нет в наличии')
