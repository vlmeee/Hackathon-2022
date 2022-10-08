from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # role = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'news'


class Role(models.Model):
    title = models.CharField(max_length=255)