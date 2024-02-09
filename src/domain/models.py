import datetime
from typing import Annotated

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .database import Base

IntPK = Annotated[int, mapped_column(primary_key=True)]


allocations = Table(
    'allocations',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('order_line_id', ForeignKey('order_lines.id'), primary_key=True),
    Column('batch_id', ForeignKey('batches.id'), primary_key=True),
)


# TODO: Разобраться с моделями, куда их перевести и где и какие модели оставить.
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

    def __repr__(self) -> str:
        return (f'<Batch('
                f'id={self.id}, '
                f'reference={self.reference}, '
                f'sku={self.sku}, '
                f'eta={self.eta}, '
                f'_purchased_quantity={self._purchased_quantity})>')
