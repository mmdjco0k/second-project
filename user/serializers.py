from rest_framework.serializers import HyperlinkedModelSerializer , HyperlinkedIdentityField , ReadOnlyField , ModelSerializer , SerializerMethodField
from post.models import PostModel
from .models import user
from django.conf import settings


class UserRetrieveSerializer(HyperlinkedModelSerializer):
    author = ReadOnlyField(source="author.username")
    class Meta:
        model = PostModel
        fields = ("description", "status", "image","postId" , "author" )

class UserList(ModelSerializer):
    posts = SerializerMethodField()

    def get_posts(self, obj):
        username = obj
        if username:
            posts = PostModel.objects.filter(author__username=username).values(
                'description',
                'status',
                'image',
                'postId'
            )
            for i in posts :
                i["image"] = f"{settings.SITE_URL}media/{i['image']}"
            return posts
        return []
    class Meta:
        model = user
        fields = ["id", "username", "first_name", "last_name", "posts"]

