from datetime import datetime

from pydantic import BaseModel


class OrderLineCreateSchema(BaseModel):
    order_id: str
    sku: str
    qty: int


class BatchCreateSchema(BaseModel):
    reference: str
    sku: str
    _purchased_quantity: int
    eta: datetime | None


class BatchSchema(BaseModel):
    reference: str
