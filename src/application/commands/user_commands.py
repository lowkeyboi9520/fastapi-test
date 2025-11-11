from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class CreateUserCommand(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    role: str = "customer"

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "password": "securepassword123",
                "phone": "+1234567890",
                "address": "123 Main St",
                "city": "New York",
                "country": "USA"
            }
        }
    }


class UpdateUserCommand(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "John Smith",
                "phone": "+1234567890",
                "address": "456 Oak Ave"
            }
        }
    }


class DeleteUserCommand(BaseModel):
    user_id: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1
            }
        }
    }