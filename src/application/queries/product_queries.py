from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GetProductQuery(BaseModel):
    product_id: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1
            }
        }
    }


class GetProductsQuery(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    category_id: Optional[int] = Field(None, gt=0)
    is_active: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "skip": 0,
                "limit": 20,
                "category_id": 1,
                "is_active": True
            }
        }
    }


class SearchProductsQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=100)
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "wireless",
                "skip": 0,
                "limit": 10
            }
        }
    }


class ProductDTO(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    sku: str
    is_active: bool
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True