from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class OrderLineCreateSchema(BaseModel):
    order_id: str
    sku: str
    qty: int


class BatchCreateSchema(BaseModel):
    reference: str
    sku: str
    purchased_quantity: int = Field(alias='_purchased_quantity')
    eta: datetime | None


class BatchSchema(BaseModel):
    reference: str
