from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import registry

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


def start_mappers() -> None:
    """
    see more about 'classical mapping':
    https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#classical-mappings
    """

    lines_mapper: Mapper = mapper_registry.map_imperatively(OrderLine, order_lines)

