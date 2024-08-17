from ninja import Router, Form
from .schemas import UserSchema, UserTokenSchema
from .models import User
from api_ecommerce.security import (BaseJWT, AuthTokenBearer)
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.db import IntegrityError


auth_router = Router()

@auth_router.post("/register")
def register(request, payload: UserSchema):
    try:
        user = User.objects.create_user(**payload.dict())
        return {
            "status": "success",
            "data": {
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "phone": user.phone,
                "password": user.password
            }
        }
    except IntegrityError:
        return {"error": "User already exists"}
    


@auth_router.post("/login")
def login(request, payload: UserTokenSchema):
    try:
        user = User.objects.get(username=payload.username)
        if not user.check_password(payload.password):
            return {"error": "Invalid password"}
        return {
            "user": user.username,
            "token": BaseJWT.create_token({"username": user.username,
                                        "password": user.password})  
        }
        
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    
   
@auth_router.get("/get-user-info", auth=AuthTokenBearer())
def get_user_info(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'Bearer ' not in auth_header:
        raise HttpError(401, "Authorization header missing or malformed.")
    
    token = auth_header.split('Bearer ')[1]
    decoded = BaseJWT.get_info(token)
    if not decoded:
        raise HttpError(401, "Invalid or expired token.")

    username = decoded.get('username')
    try:
        user = get_object_or_404(User, username=username)
        return {
            "status": "User found",
            "data": {
                "email": user.email,
                "exp": request.expire_datetime
            }
        }
    except User.DoesNotExist:
        raise HttpError(404, "User not found")

