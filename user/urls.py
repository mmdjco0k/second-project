from .views import ReadUser
from django.urls import path , include

app_name = "apiUser"

urlpatterns = [
    path('users/', ReadUser.as_view({"get": "get"}), name="list"),
    path('user/<slug:slug>/', ReadUser.as_view({"get":"retrieve"}), name = "detail"),
]
