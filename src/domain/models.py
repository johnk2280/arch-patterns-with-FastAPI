import datetime
from typing import Annotated
from typing import Any

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

IntPK = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


allocations = Table(
    'allocations',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('order_line_id', ForeignKey('order_lines.id'), primary_key=True),
    Column('batch_id', ForeignKey('batches.id'), primary_key=True),
)


class OrderLine(Base):

    __tablename__ = 'order_lines'

    id: Mapped[IntPK]
    sku: Mapped[str]
    qty: Mapped[int]
    order_id: Mapped[str]
    batches: Mapped[list['Batch']] = relationship(
        secondary=allocations,
        back_populates='_allocations',
    )

    def __repr__(self) -> str:
        return (f'<OrderLine('
                f'id={self.id}, '
                f'sku={self.sku}, '
                f'qty={self.qty}, '
                f'order_id={self.order_id})>')


# TODO: заменить модель Batch на эту модель и прогнать тесты
class Batch(Base):

    __tablename__ = 'batches'

    id: Mapped[IntPK]
    reference: Mapped[str]
    sku: Mapped[str]
    eta: Mapped[datetime.date | None]
    _purchased_quantity: Mapped[int]
    _allocations: Mapped[set['OrderLine']] = relationship(
        secondary=allocations,
        back_populates='batches',
    )

    # TODO: пересмотреть
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
        return (f'<Batch('
                f'id={self.id}, '
                f'reference={self.reference}, '
                f'sku={self.sku}, '
                f'eta={self.eta}, '
                f'_purchased_quantity={self._purchased_quantity})>')

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
