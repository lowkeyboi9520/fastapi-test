from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GetOrderQuery(BaseModel):
    order_id: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "order_id": 1
            }
        }
    }


class GetOrdersQuery(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    status: Optional[str] = Field(None, pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")

    model_config = {
        "json_schema_extra": {
            "example": {
                "skip": 0,
                "limit": 20,
                "status": "pending"
            }
        }
    }


class GetUserOrdersQuery(BaseModel):
    user_id: int = Field(..., gt=0)
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "skip": 0,
                "limit": 10
            }
        }
    }


class OrderItemDTO(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class OrderDTO(BaseModel):
    id: int
    order_number: str
    user_id: int
    status: str
    payment_method: str
    subtotal: float
    tax_amount: float
    shipping_cost: float
    total_amount: float
    shipping_address: str
    billing_address: str
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemDTO]

    class Config:
        from_attributes = True