from django.db import models
from batches.models import Batch
from users.models import User
from assignments.models import Tag
from institutes.models import Institute

# Create your models here.

class Post(models.Model):
    ACCESS_LEVEL_CHOICES = [('batch', 'Batch'), ('institute', 'Institute'), ('global', 'Global')]

    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    img_urls = models.TextField(blank=True, null=True)  # Assuming 'text ARRAY' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='posts')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='posts')
    access_level = models.CharField(max_length=9, choices=ACCESS_LEVEL_CHOICES, default='batch')
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='post_likes')



class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='replies')
    depth = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    img_urls = models.TextField(blank=True, null=True)  # Assuming 'text ARRAY' means array of text, Django doesn't support array fields natively. You might need to use JSONField or a third-party library for this.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='post_comments')
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class PostTagMapping(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='post_tag_mappings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tag_mappings')
    is_deleted = models.BooleanField(default=False)