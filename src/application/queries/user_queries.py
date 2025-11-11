from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class GetUserQuery(BaseModel):
    user_id: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1
            }
        }
    }


class GetUsersQuery(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    role: Optional[str] = Field(None, pattern="^(customer|admin|moderator)$")
    is_active: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "skip": 0,
                "limit": 20,
                "role": "customer",
                "is_active": True
            }
        }
    }


class UserDTO(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True