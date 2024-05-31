import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


JWT_AUTH = settings.JWT_AUTH
SECRET_KEY = settings.SECRET_KEY


@database_sync_to_async
def get_user(token_key):

    # If you are using jwt
    try:
        user_id: int = jwt.decode(token_key, SECRET_KEY, algorithms=[
                                  JWT_AUTH['JWT_ALGORITHM']]).get('user_id')
    except jwt.exceptions.DecodeError:
        return AnonymousUser()
    except jwt.exceptions.ExpiredSignatureError:
        return AnonymousUser()

    try:
        return AnonymousUser() if user_id is None else User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


"""
    This is a middleware to authenticate a request's user.
    If the request's user is authenticated then it will set
    the user in 'scope' so that we can access it in consumer
    otherwise it will set AnonymousUser in 'scope'.
"""


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split(
                "&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
