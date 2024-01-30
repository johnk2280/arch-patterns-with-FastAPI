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


def insert_batch(session: Session, batch_id: str) -> str:
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        ),
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        text(
            'SELECT id FROM batches WHERE reference=:batch_id AND '
            'sku="GENERIC-SOFA"',
        ),
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(
    session: Session,
    order_line_id: str,
    batch_id: str,
) -> None:
    session.execute(
        text(
            "INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)",
        ),
        dict(orderline_id=order_line_id, batch_id=batch_id),
    )
