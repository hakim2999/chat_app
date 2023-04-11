from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.get(id=token.user_id)
        if not user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        return (user, token)
