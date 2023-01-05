from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt

from users.models import User
from api.settings import JWT_KEY

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if len(auth_header) < 2:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth_header[1]
            id = jwt.decode(token, JWT_KEY, algorithms=['HS256']).get('id', None)
            if id is None:
                raise User.DoesNotExist
            user = User.objects.get(pk=id)
            
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, token)