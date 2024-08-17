from ninja import Schema, ModelSchema
from .models import User
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'username', 'full_name']
        
class UserTokenSchema(Schema):
    username: str
    password: str   