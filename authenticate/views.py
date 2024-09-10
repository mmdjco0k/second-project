from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .custom_auth import CustomAuthentication

class CustomTokenObtainPairView(TokenObtainPairView):
    authentication_class = CustomAuthentication

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('access')
        http_response = HttpResponse()
        http_response.set_cookie('access', token, httponly=True, domain="127.0.0.1", path="/", secure=False)
        refresh_token = response.data.get('refresh')
        http_response.set_cookie('refresh', refresh_token, httponly=True)
        return http_response

