from rest_framework.serializers import HyperlinkedModelSerializer , HyperlinkedIdentityField , ReadOnlyField , ModelSerializer , SerializerMethodField
from post.models import Post
from .models import user
from django.conf import settings


class UserRetrieveSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="apipost:detail",
        lookup_field="pk",
    )

    def get_likes(self, obj):
        likes = obj.likes.count()
        return likes
    likes = SerializerMethodField("get_likes")
    author = ReadOnlyField(source="author.username")
    class Meta:
        model = Post
        fields = ("description", "status", "image","postId" , "author" , "url"  , "likes")

class UserList(ModelSerializer):
    posts = SerializerMethodField("get_posts")
    url = HyperlinkedIdentityField(view_name="apiuser:detail" , lookup_field="username",)


    def get_posts(self, obj):
        username = obj
        if username:
            posts = Post.objects.filter(author__username=username).values(
                'description',
                'status',
                'image',
                'postId' ,
            )
            for i in posts :
                i["image"] = f"{settings.SITE_URL}media/{i['image']}"
            return posts
        return []
    class Meta:
        model = user
        fields = ["id", "username", "first_name", "last_name" , "url", "posts"]