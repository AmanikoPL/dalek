from pydantic import BaseModel
from typing import Optional, List

class GameSchema(BaseModel):
    title: str
    platform: str
    price: Optional[int]
    availability: bool
    image_url: Optional[str]