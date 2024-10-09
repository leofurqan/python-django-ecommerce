from base64 import b64decode
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

class BasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        if not auth_header:
            return None
        
        try:
            auth_type, credentials = auth_header.split()
            if auth_type.lower() != 'basic':
                return None
            username, password = b64decode(credentials).decode('utf-8').split(':')
            user = User.objects.get(username=username)
            if user.check_password(password):
                return (user, None)
            else:
                raise AuthenticationFailed({'detail': 'Invalid credentials.'})
        except(TypeError, ValueError, UnicodeDecodeError):
            return None
        except User.DoesNotExist:
            raise AuthenticationFailed({'detail': 'Invalid credentials.'})
