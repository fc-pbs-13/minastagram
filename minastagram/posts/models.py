from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from users.models import User


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='media')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(User, related_name='like_posts')


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply')
    author = models.ForeignKey(User, on_delete=models.CASCADE, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             # related name, related_query_name 은 역방향 테이블을 위한 값.
                             related_name='comments',
                             null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, )
    count = models.IntegerField(default=0)
