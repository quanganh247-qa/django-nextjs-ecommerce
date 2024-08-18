from .models import *
from ninja import ModelSchema, Schema
from api_ecommerce.user.schema import UserSchema
from typing import List

class ItemSchema(Schema):
    id: int
    title: str
    price: float
    discount_price: float
    category: str
    label: str
    slug: str
    description: str
    image: str
    
class OrderItemSchema(Schema):
    id: int
    item: ItemSchema
    quantity: int
    user: UserSchema
    ordered: bool

    
    
class OrderSchema(Schema):
    id: int
    user: int
    items: List[OrderItemSchema]
    ordered: bool
    ordered_date: str
    total_price: float
    
class AddressReqestSchema(Schema):
    user_id : int
    street_address: str
    apartment_address: str
    country: str
    zip: str
    address_type: str
    
class AddressSchema(ModelSchema):
    class Meta:
        model = Address
        fields = '__all__'
