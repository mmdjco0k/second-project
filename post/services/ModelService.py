from django.db.models import QuerySet, Manager, Q
from django.db import models

class SoftQuery(QuerySet):
    def delete(self):
        self.update(is_deleted=True , status=False,)

class SoftManager(Manager):
    def get_queryset(self):
        return SoftQuery(self.model , self._db).filter(Q(is_deleted = False) | Q(is_deleted__isnull = True))


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

class RecycleManager(Manager):
    def get_queryset(self):
        return self._queryset_class(self.model , self._db).filter(Q(is_deleted = True) | Q(is_deleted__isnull = False))