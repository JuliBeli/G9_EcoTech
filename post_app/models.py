import logging

from django.db import models
import json
# Create your models here.

class PostRaw(models.Model):
    userid = models.CharField(max_length=20)
    username = models.CharField(max_length=45)
    post_time = models.CharField(max_length=45)
    thumbs_up_int = models.IntegerField(default=0)
    content = models.TextField()
    title = models.TextField(max_length=30, default='New Post')

    DATA_TYPE_CHOICES = [
        (1, 'admin'),
        (2, 'user'),
    ]
    data_type = models.CharField(max_length=1, choices=DATA_TYPE_CHOICES, default=2)

    class Meta:
        app_label = 'post_app'
        db_table = 'post_app_raw'
        verbose_name = 'Post Data Management'
        # ordering = ['id', 'userid', 'username', 'user_gender', 'user_followers', 'post_time', 'thumbs_up', 'reposts', 'comments', 'user_followers_int', 'thumbs_up_int', 'reposts_int', 'comments_int', 'content']

    def short_content(self):
        # print(f'Original content length: {len(str(self.content))}')
        short_content = str(self.content)[0:100] if len(str(self.content)) > 100 else str(self.content)
        # print(f'Shortened content length: {len(short_content)}')
        return short_content + '...' if len(str(self.content)) > 100 else short_content

