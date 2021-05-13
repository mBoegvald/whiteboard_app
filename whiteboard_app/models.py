from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import related

from embed_video.fields import EmbedVideoField


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    url = EmbedVideoField(null=True)

    @classmethod
    def create_post(cls, user, text, url):
        post = cls()
        post.user = user
        post.text = text
        if url:
            post.url = url
        post.save()


# The Comment model is attached to a user and a post, which allows me
# to connect the comments for each post (with ForeignKeys)
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    text = models.CharField(max_length=280)
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')

    @classmethod
    def create_comment(cls, user, text, post):
        comment = cls()
        comment.user = user
        comment.text = text
        comment.post = post
        comment.save()
