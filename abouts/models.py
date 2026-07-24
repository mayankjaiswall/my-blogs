from django.db import models

# Create your models here.

class About(models.Model):
    about_title = models.CharField(max_length=30)
    about_description = models.TextField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.about_title
