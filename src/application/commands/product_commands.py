from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateProductCommand(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    sku: str = Field(..., min_length=1, max_length=100)
    category_id: int = Field(..., gt=0)
    is_active: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Wireless Headphones",
                "description": "High-quality wireless headphones with noise cancellation",
                "price": 199.99,
                "stock_quantity": 100,
                "sku": "WH-001",
                "category_id": 1,
                "is_active": True
            }
        }
    }


class UpdateProductCommand(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    category_id: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Wireless Headphones Pro",
                "price": 249.99,
                "stock_quantity": 50
            }
        }
    }


class DeleteProductCommand(BaseModel):
    product_id: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1
            }
        }
    }