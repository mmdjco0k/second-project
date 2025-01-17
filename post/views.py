from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .services.ViewService import ReadViewService , ChangesViewService , LikePosts
from rest_framework.viewsets import ViewSet , ModelViewSet
from rest_framework.permissions import  AllowAny
from .serializers import ReadPostSerilizer
from.models import Post
import logging

class ReadPostsView(ViewSet):
    queryset = Post.objects.all()
    serializer_class = ReadPostSerilizer
    throttle_classes = [UserRateThrottle , AnonRateThrottle]
    permission_classes = [AllowAny]
    filterset_fields = ("author" , "postId")
    def get(self,request):
        response = ReadViewService.ReadPosts(self, request)
        return response

    def retrieve(self , request , pk = None):
        response = ReadViewService.retrieve(self , request , pk)
        return response

class ChangesPosts(ViewSet):
    throttle_classes = [UserRateThrottle]

    def create(self , request):
        response = ChangesViewService.CreatePost(self , request)
        return  response

    def update(self , request ,pk=None):
        response = ChangesViewService.PartialUpdate(self , request,pk)
        return response
    def delete(self , request , pk):
        response = ChangesViewService.Delete(self  , request , pk)
        return response

class LikePostsView(ViewSet):
    throttle_classes = [UserRateThrottle]
    def post(self , request , pk = None):
            response = LikePosts.like(request , pk)
            return response