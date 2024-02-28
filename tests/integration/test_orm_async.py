from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import OrderLine


async def test_order_line_mapper_can_load_lines_async(
    async_session: AsyncSession,
):
    await async_session.execute(
        insert(order_lines)
        .values(
            [
                {
                    'order_id': 'order-1',
                    'sku': 'RED-CHAIR',
                    'qty': 12,
                },
                {
                    'order_id': 'order-2',
                    'sku': 'RED-TABLE',
                    'qty': 13,
                },
                {
                    'order_id': 'order-3',
                    'sku': 'BLUE-LIPSTICK',
                    'qty': 14,
                },

            ]
        )
    )

    expected = [
        OrderLine('order-1', 'RED-CHAIR', 12),
        OrderLine('order-2', 'RED-TABLE', 13),
        OrderLine('order-3', 'BLUE-LIPSTICK', 14),
    ]

    order_lines = (
        await async_session.execute(select(OrderLine))
    ).scalars().all(

    )

    assert order_lines == expected


# def test_order_line_mapper_can_save_lines(session: Session):
#     new_line = OrderLine('order-1', 'RED-CHAIR', 12)
#     session.add(new_line)
#     session.commit()
#
#     rows = session.query(OrderLine).all()
#
#     assert len(rows) == 1
#     assert rows[0] == new_line
