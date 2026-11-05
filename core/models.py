from pydantic import BaseModel, Field


class GroceryItem(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=80)
    quantity: str = Field(default="", max_length=60)
    purchased: bool = False
