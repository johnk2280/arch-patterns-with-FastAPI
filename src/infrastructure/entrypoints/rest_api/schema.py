from pydantic import BaseModel


class OrderLineCreateSchema(BaseModel):
    order_id: str
    sku: str
    qty: int
