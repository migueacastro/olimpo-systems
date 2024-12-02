from django.conf import settings
from datetime import datetime
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
import jwt, threading

# This function will create a access token hash containing the user id and expiration date
def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + settings.TOKEN_DURATION, # The token will have a duration of the specified setting
        'iat': datetime.now()
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

def get_user_from_token(request):
    user_token = request.COOKIES.get('access_token')
    if user_token:
        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
            expiration_time = datetime.fromtimestamp(payload['exp'])
            if expiration_time > datetime.now():
                user_model = get_user_model()
                user = user_model.objects.filter(id=payload['user_id']).first()
                return user
            else:
                raise AuthenticationFailed('Token has expired')
        except jwt.ExpiredSignatureError:
            response = Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('access_token')
            return response

def user_is_allowed(user_instance, superuser_only=False):
    return user_instance.is_admin or (user_instance.is_superuser and not superuser_only) 
