# Register your models here.
from django.contrib import admin
from .models import PostRaw
import re
from django.contrib import messages

class PostAdmin(admin.ModelAdmin):
    list_display = (
    'author', 'title','created_at', 'likes_int',
    'display_short_content', 'post_type')
    list_filter = ('post_type',)
    def display_short_content(self, obj):
        return obj.short_content()
    display_short_content.short_description = 'Short Content'
    def has_change_permission(self, request, obj=None):
        if request.method == 'POST':
            return True
        return super().has_change_permission(request, obj)


admin.site.register(PostRaw, PostAdmin)
