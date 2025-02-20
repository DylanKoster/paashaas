from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
from datetime import datetime, timedelta

ORDER_EXPIRY_MINUTES = 15

class OrderItem(BaseModel):
    item_id: str
    quantity: int


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    store_id: str = ""
    creation_date: datetime = Field(default_factory=datetime.now)
    expiry_date: datetime = Field(default_factory=lambda x: datetime.now() + timedelta(minutes=ORDER_EXPIRY_MINUTES))
    status: str = Field(default="pending")
    items: list[OrderItem] = []

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = ["pending", "completed", "cancelled"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v