from ninja import Router
from api_ecommerce.security import (BaseJWT, AuthTokenBearer)
from typing import List
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib import messages
from datetime import datetime,timezone
from .schemas import *
from django.db import transaction

order_router = Router()


@transaction.atomic
@order_router.get("/get-carts", response=List[OrderItemSchema], auth=AuthTokenBearer())
def get_cart(request):
    user = request.user
    carts = OrderItem.objects.filter(user=user, ordered=False)

    # Convert QuerySet to a list of dictionaries
    carts_list = [
        {
            "id": cart.id,
            "item":{
                "id": cart.item.id,
                "title": cart.item.title,
                "price": cart.item.price,
                "discount_price": cart.item.discount_price,
                "category": cart.item.category,
                "label": cart.item.label,
                "slug": cart.item.slug,
                "description": cart.item.description,
                "image": cart.item.image,   
            
                }, 
            "quantity": cart.quantity,
            "user": {
                "id": cart.user.id,
                "username": cart.user.username,
                "email": cart.user.email,
                "full_name": cart.user.full_name,
            },
            "ordered": cart.ordered,
        }
        for cart in carts
    ]

    return carts_list

@transaction.atomic
@order_router.post("/add-to-cart", response=OrderSchema, auth=AuthTokenBearer())   
def add_to_cart(request, slug: str):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
    else:
        ordered_date = datetime.now(timezone.utc)  # Use datetime.now with timezone.utc
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")

    # Construct the response
    order_data = {
        "id": order.id,
        "user": order.user.id,
        "items": [
            {
                "id": order_item.id,
                "item": {
                    "id": order_item.item.id,
                    "title": order_item.item.title,
                    "price": order_item.item.price,
                    "discount_price": order_item.item.discount_price,
                    "category": order_item.item.category,
                    "label": order_item.item.label,
                    "slug": order_item.item.slug,
                    "description": order_item.item.description,
                    "image": str(order_item.item.image.url),  # Ensure image is a string (URL)
                },
                "quantity": order_item.quantity,
                "user": {
                    "id": order_item.user.id,
                    "username": order_item.user.username,
                    "email": order_item.user.email,
                    "full_name": order_item.user.full_name,
                },
                "ordered": order_item.ordered,
            }
        ],
        "ordered": order.ordered,
        "ordered_date": order.ordered_date.strftime("%Y-%m-%d %H:%M:%S"),
        "total_price": order.get_total()
    }

    return order_data

@transaction.atomic
@order_router.post("/remove-from-cart",auth=AuthTokenBearer())
def remove_from_cart(request, slug: str):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(itemm__slug= item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
        else:
            messages.info(request, "This item was not in your cart.")
    else:
        messages.info(request, "You do not have an active order.")
        


@transaction.atomic
@order_router.post("/remove-single-item-from-cart",auth=AuthTokenBearer())
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity>1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "This item quantity was updated.")
    else:
        messages.info(request, "You do not have an active order.")
        
        
def get_coupon(request, code):
    try:
        coupon = get_object_or_404(Coupon, code=code)
        return coupon
    except Coupon.DoesNotExist:
        messages.info(request, "This coupon does not exist.")
        return None
    
@transaction.atomic
@order_router.post("/add-coupon",response=OrderSchema,auth=AuthTokenBearer())
def add_coupon(request, code):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        coupon = get_coupon(request, code)
        if coupon:
            order.coupon = coupon
            order.save()
            messages.info(request, "Coupon added successfully.")
    return order
            