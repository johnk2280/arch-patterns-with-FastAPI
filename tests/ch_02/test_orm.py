from sqlalchemy import text
from sqlalchemy.orm import Session

from domain.model import OrderLine


def test_order_line_mapper_can_load_lines(session: Session):
    session.execute(
        text(
            "INSERT INTO order_lines (order_id, sku, qty) VALUES "
            '("order-1", "RED-CHAIR", 12), '
            '("order-2", "RED-TABLE", 13), '
            '("order-3", "BLUE-LIPSTICK", 14) '
        ),
    )
    expected = [
        OrderLine('order-1', 'RED-CHAIR', 12),
        OrderLine('order-2', 'RED-TABLE', 13),
        OrderLine('order-3', 'BLUE-LIPSTICK', 14),
    ]

    assert session.query(OrderLine).all() == expected


def test_order_line_mapper_can_save_lines(session: Session):
    new_line = OrderLine('order-1', 'RED-CHAIR', 12)
    session.add(new_line)
    session.commit()

    rows = session.query(OrderLine).all()

    assert len(rows) == 1
    assert rows[0] == new_line
