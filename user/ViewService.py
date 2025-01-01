from django.core.exceptions import ObjectDoesNotExist
from post.models import Post
from .serializers import UserRetrieveSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import user
from .serializers import UserList
class ViewUser:

    @staticmethod
    def GetList(request):
        try:
            users = user.objects.all()
            serializer = UserList(users , context={'request': request}  , many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'No users found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def Retrieve(request , slug):
        try:
            posts = Post.objects.filter(author__username=slug)
            serialized_posts = UserRetrieveSerializer(posts, many=True ,context={'request': request}).data
            return Response(serialized_posts, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'No posts found for this user'}, status=status.HTTP_404_NOT_FOUND)
