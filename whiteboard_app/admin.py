from django.contrib import admin
from .models import Post, Comment


@admin.register(Post, Comment)
class DefaultAdmin(admin.ModelAdmin):
    pass
