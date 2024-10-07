from django.db import models


class OtpModel(models.Model):
    email = models.EmailField(blank=False , null=False)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)