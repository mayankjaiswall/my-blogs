from django.db import models

# Create your models here.


class SocialPlatform(models.Model):
    platform_name = models.CharField(max_length=50, unique=True)
    platform_url = models.URLField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Social Platform'
        verbose_name_plural = 'Social Platforms'

    def __str__(self):
        return self.platform_name