from collections.abc import Sequence

from domain import Batch


def is_valid_sku(sku: str, batches: Sequence[Batch]) -> bool:
    return sku in {b.sku for b in batches}