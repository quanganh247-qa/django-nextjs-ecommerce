from ninja.security import HttpBearer
from ..jwt import BaseJWT   
from web_app.models import User
import logging
logger = logging.getLogger(__name__)
class AuthTokenBearer(HttpBearer):
    data_user = None
    def authenticate(self, request, token):
        decode_token = BaseJWT.get_info(token)
        username = decode_token.get('username',None)
        logger.info("decode_token %s",username )
        
        if username:
            request.user = User.objects.get(username=username) if AuthTokenBearer.data_user is None else AuthTokenBearer.data_user
            AuthTokenBearer.data_user = request.user
            request.expire_datetime = decode_token.get('expire_datetime',None)
            return True
        return False