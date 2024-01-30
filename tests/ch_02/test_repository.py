from sqlalchemy import insert
from sqlalchemy import text
from sqlalchemy.orm import Session

from ch_02.model import OrderLine
from ch_02.repository import SQLAlchemyRepository


def test_repository_can_save_a_batch(session: Session):
    from ch_02.model import Batch
    batch = Batch('batch-1', 'RUSTY-SOAPDISH', 100)
    repo = SQLAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.query(Batch).all()

    assert len(rows) == 1
    assert rows == [batch]


def insert_order_line(session: Session) -> str:
    session.execute(
        text(
            'INSERT INTO order_lines (orderid, sku, qty)'
            ' VALUES ("order1", "GENERIC-SOFA", 12)',
        ),
    )
    [[order_line_id]] = session.execute(
        text(
            "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        ),
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return order_line_id
