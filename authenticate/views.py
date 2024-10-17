from rest_framework_simplejwt.views import TokenObtainPairView
from .services.custom_auth import CustomAuthentication
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializer import LoginSerializer, EmailVerifySerializers
from .services.otp import OtpService
from .models import OtpModel
from .services.token import TokenService
class CustomLoginWithRegisterCode(APIView):
    CustomUser = get_user_model()
    permission_classes = [AllowAny]

    def post(self , request ):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            http_response = HttpResponse()
            username = serializer.validated_data['username']
            user = self.CustomUser.objects.filter(username=username).first()
            email = user.email
            expire_time = OtpService.request(
                email=email,
            )
            return Response({'expire_time': expire_time}, status=status.HTTP_200_OK)
        else :  return Response(serializer.errors, status=status.HTTP_200_OK)


class EmailLoginVerifyAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_class = CustomAuthentication

    CustomUser = get_user_model()

    def post(self, request):
        serializer = EmailVerifySerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data['username']
        user = self.CustomUser.objects.filter(username=username).first()
        if user is None:
            return Response({'detail': 'OTP Not Exists'}, status=status.HTTP_404_NOT_FOUND)
        email = user.email
        otp_code = serializer.validated_data.get('code')
        user_obj = OtpService.verify(code=otp_code, email=email)

        if not user_obj:
            return Response({'detail': 'OTP Not Exists'}, status=status.HTTP_404_NOT_FOUND)
        otp_objs = OtpModel.objects.filter(
            code=otp_code,
            email=email,
        ).delete()

        access, refresh = TokenService.generate(user_obj)
        http_response = HttpResponse()
        http_response.set_cookie('access', access, httponly=True, domain="127.0.0.1", path="/", secure=False)
        http_response.set_cookie('refresh', refresh, httponly=True)
        return http_response