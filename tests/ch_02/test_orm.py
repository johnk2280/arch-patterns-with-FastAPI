from sqlalchemy.orm import Session

from ch_02.model import OrderLine


def test_order_line_mapper_can_load_lines(session: Session):
    session.execute(
        """
        INSERT INTO order_lines (order_id, sku, qty) VALUES
        ('order-1', 'RED-CHAIR', 12),
        ('order-2', 'RED-TABLE', 13),
        ('order-3', 'BLUE-LIPSTICK', 14),
        """
    )
    expected = [
        OrderLine('order-1', 'RED-CHAIR', 12),
        OrderLine('order-2', 'RED-TABLE', 13),
        OrderLine('order-3', 'BLUE-LIPSTICK', 14),
    ]

    assert session.query(OrderLine).all() == expected
