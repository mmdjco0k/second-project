import time
import jwt
from django.conf import settings
from django.http import HttpResponse
from user.models import user
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


secret_key = settings.SECRET_KEY


class CustomAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def authenticate(self, request):
        token = request.COOKIES.get("access")

        if token:
            validated_token = self.validate(token, request)
            if not validated_token:
                return None
            return self.get_user_custom(validated_token), validated_token
        else:
            return None

    def validate(self, token, request):
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            if "exp" in decoded_token and time.time() > decoded_token["exp"]:
                return self.get_refreshed_token(request)
            else:
                return token

        except jwt.ExpiredSignatureError:
                try:
                    return self.get_refreshed_token(request)
                except jwt.ExpiredSignatureError:
                    return False

    def get_user_custom(self, validated_token):
        token_decoded = jwt.decode(validated_token, secret_key, algorithms=["HS256"])
        id = token_decoded.get("user_id")
        User = user.objects.get(id=id)
        return User

    def get_refreshed_token(self, request):
        token = request.COOKIES.get("refresh")
        if not token:
            return HttpResponse("Refresh token not found in cookies", status=400)

        refresh_token_decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        id = refresh_token_decoded.get("user_id")
        User = user.objects.get(id=id)
        refresh_token = RefreshToken.for_user(User)
        access_token_str = str(refresh_token.access_token)

        response = HttpResponse({"msg": "Access token refreshed"})
        response.set_cookie('access', access_token_str, httponly=True, domain="127.0.0.1", path="/", secure=False)
        return self.validate(access_token_str, request)
