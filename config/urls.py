from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path , include
from authenticate.views import  CustomTokenObtainPairView , CustomLoginWithRegisterCode , EmailLoginVerifyAPIView
import logging
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('post.urls')),
    path('api/', include('user.urls')),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/', CustomLoginWithRegisterCode.as_view(), name='login'),
    path('api/login/verify/', EmailLoginVerifyAPIView.as_view(), name='login-email-verify'),

]
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
