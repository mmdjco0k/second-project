from rest_framework.serializers import (ModelSerializer , HyperlinkedModelSerializer , HyperlinkedIdentityField , IntegerField , SerializerMethodField)
from .models import Post
from django.db.models import Count

class CreatePostsSerilizer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("slug","description", "status", "image","postId")


class ReadPostSerilizer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="apipost:detail",
        lookup_field="pk",
    )
    like_url = HyperlinkedIdentityField(view_name="apipost:like" , lookup_field="pk")
    def get_likes(self ,obj):
        likes = obj.likes.count()
        return likes
    likes = SerializerMethodField("get_likes")
    class Meta:
        model = Post
        fields = ("slug", "description", "status", "image", "postId", "url" , "likes" , "like_url")




class PostRetrieve(HyperlinkedModelSerializer):
    def get_likes(self ,obj):
        likes = obj.likes.count()
        return likes
    likes = SerializerMethodField("get_likes")
    class Meta:
        model = Post
        fields = ("slug","description", "status", "image","postId" , "likes")


class PostSerializerPartialUpdate(ModelSerializer):
    class Meta:
        model = Post
        fields = ("slug", "description", "status", "image" , "postId")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False