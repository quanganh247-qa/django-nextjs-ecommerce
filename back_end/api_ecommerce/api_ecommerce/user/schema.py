from ninja import ModelSchema, Schema
from .models import User


class UserSchema(Schema):
    id: int
    username: str
    email: str
    full_name: str