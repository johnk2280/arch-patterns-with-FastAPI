from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import OrderLine
from infrastructure.adapters.orm import order_lines


async def test_order_line_mapper_can_load_lines_async(
    async_session: AsyncSession,
):
    await async_session.execute(
        insert(OrderLine)
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

    rows = (
        await async_session.execute(select(OrderLine))
    ).scalars().all()

    assert rows == expected


async def test_order_line_mapper_can_save_lines(
    async_session: AsyncSession,
):
    new_line = OrderLine('order-1', 'RED-CHAIR', 12)
    async_session.add(new_line)
    await async_session.commit()

    rows = (await async_session.execute(select(OrderLine))).scalars().all()

    assert len(rows) == 1
    assert rows[0] == new_line
