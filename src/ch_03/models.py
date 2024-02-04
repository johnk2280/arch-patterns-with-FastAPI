import datetime
from typing import Annotated

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import relationship

from ch_03.database import Base

IntPK = Annotated[int, mapped_column(primary_key=True)]
AllocationsFK = Annotated[int, mapped_column(
    ForeignKey('allocations.id', ondelete='CASCADE'),
)]

allocations = Table(
    'allocations',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('order_line_id', ForeignKey('order_lines.id'), primary_key=True),
    Column('batch_id', ForeignKey('batches.id'), primary_key=True),
)


class OrderLine(Base):
    __tablename__ = 'order_lines'

    id: Mapper[IntPK]
    sku: Mapper[str]
    qty: Mapper[int]
    order_id: Mapper[str]
    batches: Mapper[list['Batch']] = relationship(
        secondary=allocations,
        back_populates='_allocations',
    )


class Batch(Base):
    __tablename__ = 'batches'

    id: Mapper[IntPK]
    reference: Mapper[str]
    sku: Mapper[str]
    eta: Mapper[datetime.date | None]
    _purchased_quantity: Mapper[int]
    _allocations: Mapper[set[int]] = relationship(
        secondary=allocations,
        collection_class=set,
        back_populates='batches',
    )
