from django.db import models
from .utils.db import BaseSoftDelete , RecycleManager
from user.models import user
UserModel = user


class Post(BaseSoftDelete):
    image =models.ImageField()
    postId = models.AutoField(primary_key=True)
    description = models.CharField(null=True , max_length=255)
    slug = models.SlugField(max_length=250 , unique=True)
    likes = models.ManyToManyField(UserModel, related_name='post_likes', blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.BooleanField()



class RecyclePost(Post):
    objects = RecycleManager()
    class Meta :
        proxy = True