from .models import PostModel
from .serializers import ReadPostsSerilizer  , PostSerializerPartialUpdate
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
class ReadViewService:
    @staticmethod
    def ReadPosts(self , request):
        Products = PostModel.objects.all()
        serializer = ReadPostsSerilizer(Products, many=True, context={'request': request})
        data = serializer.data
        for i in data:
            image = i.get("image")
            i["image"] = request.build_absolute_uri(image)
        return Response(data)


class ChangesViewService:
    @staticmethod
    def CreatePost(self , request):
        data = request.data
        serializer = ReadPostsSerilizer(data=data)
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
