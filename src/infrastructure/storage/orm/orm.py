from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from domain import Batch
from domain import OrderLine
from domain.models import Product

metadata = MetaData()

mapper_registry = registry(metadata=metadata)

order_lines = Table(
    'order_lines',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('order_id', String(255)),
)

batches = Table(
    'batches',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', ForeignKey('products.sku')),
    Column('eta', Date, nullable=True),
    Column('_purchased_quantity', Integer, nullable=False),
)

allocations = Table(
    'allocations',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('order_line_id', ForeignKey('order_lines.id')),
    Column('batch_id', ForeignKey('batches.id')),
)

products = Table(
    'products',
    mapper_registry.metadata,
    Column('sku', String(255), primary_key=True),
    Column('version', Integer, nullable=False, server_default='1'),
)


def start_mappers() -> None:
    """
    see more about 'classical mapping':
    https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#classical-mappings
    """

    lines_mapper: Mapper[OrderLine] = mapper_registry.map_imperatively(
        OrderLine,
        order_lines,
    )
    batch_mapper: Mapper[Batch] = mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            '_allocations': relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            ),
        },
    )
    mapper_registry.map_imperatively(
        Product,
        products,
        properties={'batches': relationship(batch_mapper)},
    )
