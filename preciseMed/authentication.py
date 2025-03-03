import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import ExpiredSignatureError
from rest_framework import authentication, status
from rest_framework.exceptions import ParseError, APIException

User = get_user_model()

class CustomNotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Incorrect authentication credentials.'
    default_code = 'not_authenticated'


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise CustomNotAuthenticated()
        except ExpiredSignatureError:
            raise CustomNotAuthenticated()
        except:
            raise ParseError()

        # Get the user from the database
        username_or_phone_number = payload.get('username')
        if username_or_phone_number is None:
            raise CustomNotAuthenticated()

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            raise CustomNotAuthenticated()


        # Return the user and token payload
        return user, payload

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token