import datetime
from dataclasses import dataclass


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
        self.available_quantity = qty

    def allocate(self, line: OrderLine) -> None:
        self.available_quantity -= line.qty


def make_batch_and_line(
    sku: str,
    batch_qty: int,
    line_qty: int,
) -> tuple[Batch, OrderLine]:
    return (
        Batch('batch-001', sku, batch_qty, eta=datetime.date.today()),
        OrderLine('order-123', sku, line_qty)
    )

