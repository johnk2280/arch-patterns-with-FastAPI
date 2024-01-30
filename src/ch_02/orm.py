from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import registry

from ch_02.model import Batch
from ch_02.model import OrderLine

metadata = MetaData()

# mapper_registry = registry(metadata=metadata)
mapper_registry = registry()

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
    Column('sku', String(255)),
    Column('eta', Date, nullable=True),
    Column('_purchased_quantity', Integer, nullable=False),
)


def start_mappers() -> None:
    """
    see more about 'classical mapping':
    https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#classical-mappings
    """

    lines_mapper: Mapper = mapper_registry.map_imperatively(
        OrderLine,
        order_lines,
    )
    mapper_registry.map_imperatively(
        Batch,
        batches,
    )
