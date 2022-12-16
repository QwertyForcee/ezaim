from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from ezaim.models import User
import jwt
from api.settings import JWT_KEY

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print('inside of jwtauth authenticate')
        auth = get_authorization_header(request).split()
        print(auth)

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            id = jwt.decode(token, JWT_KEY, algorithms=['HS256']).get('id', None)
            print('id', id)
            if id is None:
                print('id is none')
                raise User.DoesNotExist
            user = User.objects.get(pk=id)
            print('user', user)
            
        except User.DoesNotExist:
            print('user does not exist exc')
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist 

        return (user, token) # authentication successful