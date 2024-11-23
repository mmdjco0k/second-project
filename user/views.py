from rest_framework.throttling import UserRateThrottle , AnonRateThrottle
from rest_framework.viewsets import ViewSet
from .ViewService import ViewUser
class ReadUser(ViewSet):
    throttle_classes = [UserRateThrottle]
    def get(self , request):
        return  ViewUser.GetList(request)
    def retrieve(self, request , username = None):
        return ViewUser.Retrieve(request , username)
