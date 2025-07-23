import logging
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone

import json
# Create your models here.

class PostRaw(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_int = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name = 'liked_posts', blank = True)
    content = models.TextField()
    title = models.TextField(max_length=60, blank=False, null=False)
    # images will be stored under djangoProject/media/post_images
    image = models.ImageField(upload_to='post_images/', blank=True, null=False)

    POST_TYPE_CHOICES = [
        (1, 'admin'),
        (2, 'user')
    ]

    post_type = models.IntegerField(choices=POST_TYPE_CHOICES, default=2)

    class Meta:
        app_label = 'post_app'
        db_table = 'post_app_raw'
        verbose_name = 'Post Data Management'

    def short_content(self):
        # print(f'Original content length: {len(str(self.content))}')
        short_content = str(self.content)[0:140] if len(str(self.content)) > 140 else str(self.content)
        # print(f'Shortened content length: {len(short_content)}')
        return short_content + '...' if len(str(self.content)) > 140 else short_content

    def __str__(self):
        return self.title

#reset password
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=6))