from datetime import date

from domain.model import Batch
from domain.model import make_batch_and_line
from domain.model import OrderLine


def test_allocate_to_a_batch_reduces_the_available_quantity():
    batch = Batch(
        'batch-001',
        'SMALL_TABLE',
        qty=20,
        eta=date.today(),
    )
    line = OrderLine('order-ref', 'SMALL_TABLE', 2)
    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_then_required():
    large_batch, small_line = make_batch_and_line('ELEGANT_LAMP', 20, 2)
    assert large_batch.can_allocate(small_line) is True


def test_cannot_allocate_if_available_smaller_then_required():
    large_batch, small_line = make_batch_and_line('ELEGANT_LAMP', 2, 20)
    assert large_batch.can_allocate(small_line) is False


def test_can_allocate_if_available_equal_then_required():
    large_batch, small_line = make_batch_and_line('ELEGANT_LAMP', 20, 20)
    assert large_batch.can_allocate(small_line) is True


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch('batch-001', 'UNCOMFORTABLE-CHAIR', 100)
    line = OrderLine('order-123', 'ELEGANT_LAMP', 20)
    assert batch.can_allocate(line) is False


def test_can_only_deallocate_allocated_lines():
    batch, line = make_batch_and_line('DECORATIVE-TRINKET', 20, 2)
    batch.deallocate(line)
    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    """
    Идемпотентность обеспечивается тем, что под капотом для хранения товарных
    позиций (объектов OrderLine) используется множество.
    """

    batch, line = make_batch_and_line('DECORATIVE-TRINKET', 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18
