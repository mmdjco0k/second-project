from rest_framework.serializers import (ModelSerializer , HyperlinkedModelSerializer , HyperlinkedIdentityField)
from .models import PostModel

class CreatePostsSerilizer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = ("slug","description", "status", "image","postId")


class ReadPostSerilizer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="apipost:detail",
        lookup_field="pk",
    )
    class Meta:
        model = PostModel
        fields = ("slug","description", "status", "image","postId" , "url")



class PostRetrieve(HyperlinkedModelSerializer):
    class Meta:
        model = PostModel
        fields = ("slug","description", "status", "image","postId")


class PostSerializerPartialUpdate(ModelSerializer):
    class Meta:
        model = PostModel
        fields = ("slug", "description", "status", "image" , "postId")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False