from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import OrderLine


async def test_order_line_mapper_can_load_lines_async(
    async_session: AsyncSession,
):
    expected = [
        OrderLine('order-1', 'RED-CHAIR', 12),
        OrderLine('order-2', 'RED-TABLE', 13),
        OrderLine('order-3', 'BLUE-LIPSTICK', 14),
    ]
    async_session.add_all(expected)
    await async_session.commit()

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
    assert rows[-1] == new_line
