from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CreateOrderCommand(BaseModel):
    user_id: int = Field(..., gt=0)
    payment_method: str = Field(..., pattern="^(credit_card|paypal|bank_transfer|cash_on_delivery)$")
    items: List[dict] = Field(..., min_items=1)
    shipping_address: str = Field(..., min_length=1)
    billing_address: str = Field(..., min_length=1)
    notes: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "payment_method": "credit_card",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2,
                        "unit_price": 199.99
                    }
                ],
                "shipping_address": "123 Main St, City, State 12345",
                "billing_address": "123 Main St, City, State 12345",
                "notes": "Please deliver to the front door"
            }
        }
    }


class UpdateOrderCommand(BaseModel):
    status: Optional[str] = Field(None, pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")
    payment_method: Optional[str] = Field(None, pattern="^(credit_card|paypal|bank_transfer|cash_on_delivery)$")
    notes: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "processing"
            }
        }
    }


class CancelOrderCommand(BaseModel):
    order_id: int = Field(..., gt=0)
    reason: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "order_id": 1,
                "reason": "Customer requested cancellation"
            }
        }
    }


class AddOrderItemCommand(BaseModel):
    order_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "order_id": 1,
                "product_id": 2,
                "quantity": 1,
                "unit_price": 99.99
            }
        }
    }


class UpdateOrderItemCommand(BaseModel):
    item_id: int = Field(..., gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "item_id": 1,
                "quantity": 3,
                "unit_price": 199.99
            }
        }
    }


class RemoveOrderItemCommand(BaseModel):
    item_id: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "item_id": 1
            }
        }
    }