from django.contrib import admin
from django.urls import path

from . import views

app_name = "whiteboard_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('create_post', views.createPost, name='createPost'),
    path('delete_post/<int:post_pk>', views.deletePost, name='deletePost'),
    path('create_comment', views.createComment, name='createComment'),
    path('create_user', views.createUser, name='createUser'),
    path('admin_page', views.adminPage, name='adminPage'),
]
