from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

class Store(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    location: str
