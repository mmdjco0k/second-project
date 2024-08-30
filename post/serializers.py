from rest_framework.serializers import ModelSerializer
from .models import PostModel

class ReadPostsSerilizer(ModelSerializer):
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