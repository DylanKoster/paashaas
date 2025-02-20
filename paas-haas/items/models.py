from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    img: str = ""


class InventoryItem(Item):
    store_id: str = ""
    quantity: int