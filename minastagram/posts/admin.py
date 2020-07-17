from django.contrib import admin
from posts.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'text', 'created_date', ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'text', 'created_date', ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
