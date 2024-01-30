from sqlalchemy import text
from sqlalchemy.orm import Session

from ch_02.model import Batch
from ch_02.model import OrderLine
from ch_02.repository import SQLAlchemyRepository


def test_repository_can_save_a_batch(session: Session):
    batch = Batch('batch-1', 'RUSTY-SOAPDISH', 100)
    repo = SQLAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.query(Batch).all()

    assert len(rows) == 1
    assert rows == [batch]


def insert_order_line(session: Session) -> int:
    session.execute(
        text(
            'INSERT INTO order_lines (order_id, sku, qty)'
            ' VALUES ("order1", "GENERIC-SOFA", 12)',
        ),
    )
    [[order_line_id]] = session.execute(
        text(
            "SELECT id FROM order_lines WHERE order_id=:order_id AND sku=:sku",
        ),
        dict(order_id="order1", sku="GENERIC-SOFA"),
    )
    return order_line_id


def insert_batch(session: Session, batch_id: str) -> int:
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
    order_line_id: int,
    batch_id: int,
) -> None:
    session.execute(
        text(
            "INSERT INTO allocations (order_line_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)",
        ),
        dict(orderline_id=order_line_id, batch_id=batch_id),
    )


def test_repository_can_retrieve_a_batch_with_allocations(session: Session):
    order_line_id = insert_order_line(session)
    batch_id_1 = insert_batch(session, 'batch-1')
    insert_batch(session, 'batch-2')
    insert_allocation(session, order_line_id, batch_id_1)

    repo = SQLAlchemyRepository(session)
    retrieved = repo.get('batch-1')

    expected = Batch('batch-1', 'GENERIC-SOFA', 100)

    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine('order1', 'GENERIC-SOFA', 12),
    }
