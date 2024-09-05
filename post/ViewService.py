from django.db.models import Count

from .models import PostModel
from .serializers import CreatePostsSerilizer  , PostSerializerPartialUpdate , PostRetrieve , ReadPostSerilizer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
class ReadViewService:
    @staticmethod
    def ReadPosts(self , request):
        posts = PostModel.objects.all()
        serializer = ReadPostSerilizer(posts, many=True, context={'request': request})
        data = serializer.data
        for i in data:
            image = i.get("image")
            i["image"] = request.build_absolute_uri(image)
        return Response(data)
    @staticmethod
    def retrieve(self, request, pk):
        product = get_object_or_404(PostModel, pk=pk)
        serializer = PostRetrieve(product, context={"request": request})
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
class ChangesViewService:
    @staticmethod
    def CreatePost(self , request):
        data = request.data
        serializer = CreatePostsSerilizer(data=data)
        if serializer.is_valid():
            user = request.user
            serializer.validated_data["author"] = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def PartialUpdate(self , request , pk):
        post =get_object_or_404(PostModel ,pk=pk )
        serializer = PostSerializerPartialUpdate(post , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def Delete(self , request , pk ):
        post = get_object_or_404(PostModel , pk = pk )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikePosts:
    @staticmethod
    def like(request , pk ):
        post = get_object_or_404(PostModel , pk = pk)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response("Removed like.", status=status.HTTP_201_CREATED)
        else :
            post.likes.add(user)
            return Response("add like.", status=status.HTTP_201_CREATED)
