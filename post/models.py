from django.db import models
from .services.ModelService import SoftDeleted , RecycleManager
from user.models import user
UserModel = user


class PostModel(SoftDeleted):
    image =models.ImageField()
    postId = models.AutoField(primary_key=True)
    description = models.CharField(null=True , max_length=255)
    slug = models.SlugField(max_length=250 , unique=True)
    likes = models.ManyToManyField(UserModel, related_name='post_likes', blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.BooleanField()



class RecyclePost(PostModel):
    objects = RecycleManager()
    class Meta :
        proxy = True