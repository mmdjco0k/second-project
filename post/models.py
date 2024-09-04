from django.db import models
from django.db.models import Q , QuerySet , Manager
from django.contrib.auth import get_user_model
from user.models import user
UserModel = user

class SoftManager(Manager):
    def get_queryset(self):
        return QuerySet(self.model , self._db).filter(Q(is_deleted = False) | Q(is_deleted__isnull = True))


class SoftDeleted(models.Model):
    is_deleted = models.BooleanField(default=False , null=True)
    status = models.BooleanField(default=False)
    objects = SoftManager()
    class Meta:
        abstract = True
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.status = False
        self.save()

class PostModel(SoftDeleted):
    image =models.ImageField()
    postId = models.AutoField(primary_key=True)
    description = models.CharField(null=True , max_length=255)
    slug = models.SlugField(max_length=250 , unique=True)
    likes = models.ManyToManyField(UserModel, related_name='post_likes', blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.BooleanField()


class RecycleManager(Manager):
    def get_queryset(self):
        return self._queryset_class(self.model , self._db).filter(Q(is_deleted = True) | Q(is_deleted__isnull = False))

class RecyclePost(PostModel):
    objects = RecycleManager()
    class Meta :
        proxy = True