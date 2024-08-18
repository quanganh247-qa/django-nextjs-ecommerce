from ninja import Router
from api_ecommerce.security import (BaseJWT, AuthTokenBearer)
from typing import List
from .schemas import ItemSchema
from .models import Item

item_router = Router()

@item_router.get("/get-items", response=List[ItemSchema],auth=AuthTokenBearer())
def get_items(request):
    return Item.objects.all()

@item_router.get("/get-item/{slug}", response=ItemSchema,auth=AuthTokenBearer())
def get_item(request, slug: str):
    return Item.objects.get(slug=slug)