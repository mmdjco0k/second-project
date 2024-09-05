from .views import ReadUser
from django.urls import path , include

app_name = "apiuser"

urlpatterns = [
    path('users/', ReadUser.as_view({"get": "get"}), name="list"),
    path('user/<str:username>/', ReadUser.as_view({"get":"retrieve"}), name = "detail"),
]
