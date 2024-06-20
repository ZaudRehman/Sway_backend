# backend/models/order_details.py

from typing import List
from pydantic import BaseModel
from .cart import Cart

class OrderDetails(BaseModel):
    user_id: str
    total_cost: float
    cart_items: List[Cart]

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types in Pydantic models
        orm_mode = True
