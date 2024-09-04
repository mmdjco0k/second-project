from rest_framework.viewsets import ViewSet
from .ViewService import ViewUser
class ReadUser(ViewSet):
    def get(self , request):
        return  ViewUser.GetList(request)
    def retrieve(self, request , slug = None):
        return ViewUser.Retrieve(request , slug)
