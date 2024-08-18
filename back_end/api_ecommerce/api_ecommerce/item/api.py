from ninja import Router
from api_ecommerce.security import (BaseJWT, AuthTokenBearer)
from typing import List
from .schemas import ItemSchema
from .models import Item

item_router = Router()

@item_router.get("/get-items", response=List[ItemSchema],auth=AuthTokenBearer())
def get_items(request):
    return Item.objects.all()