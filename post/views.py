from .ViewService import ReadViewService , ChangesViewService
from rest_framework.viewsets import ViewSet , ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny , IsAuthenticatedOrReadOnly
from .serializers import ReadPostsSerilizer
from.models import PostModel
class ReadPostsView(ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = ReadPostsSerilizer
    permission_classes = [AllowAny]

    def get(self,request):
        response = ReadViewService.ReadPosts(self, request)
        return response

class ChangesPosts(ViewSet):
    def create(self , request):
        response = ChangesViewService.CreatePost(self , request)
        return  response

    def update(self , request ,pk=None):
        response = ChangesViewService.PartialUpdate(self , request,pk)
        return response
    def delete(self , request , pk):
        response = ChangesViewService.Delete(self  , request , pk)
        return response