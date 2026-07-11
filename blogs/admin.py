from django.contrib import admin

from .models import Blog, Category
# Register your models here.

class BlogAuto(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'created_at')

admin.site.register(Category)
admin.site.register(Blog, BlogAuto)