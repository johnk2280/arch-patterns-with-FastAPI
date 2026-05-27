from datetime import date  # noqa: TC003

from ..base import DomainModel


class Batch(DomainModel):
    def __init__(self, ref: str, sku: str, qty: int, eta: date) -> None:
        self._reference = ref
        self._sku = sku
        self._qty = qty
        self._eta = eta

    @property
    def reference(self) -> str:
        return self._reference

    @property
    def sku(self) -> str:
        return self._sku

    @property
    def avaliable_quantity(self) -> int:
        return self._qty

    @property
    def eta(self) -> date:
        return self._eta
