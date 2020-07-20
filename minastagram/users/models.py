from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class User(AbstractUser):
    follow = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        is_created = self.id is None
        user = super().save()

        if is_created:
            Profile.objects.create(user=self)

        return user

    @property
    def follow(self):
        # 내가 팔로우를 건 유저
        user = User.objects.filter(
            to_users_relation__from_user=self,
            to_users_relation__related_type='f'
        )
        return user

    @property
    def follower(self):
        # 나를 팔로우를 건 유저
        user = User.objects.filter(
            from_users_relation__to_user=self,
            from_users_relation__related_type='f'
        )
        return user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    nickname = models.CharField(max_length=15, )
    introduce = models.CharField(max_length=100, null=True, )


class Relation(models.Model):
<<<<<<< Updated upstream
    CHOICE_RELATIONS_TYPE = (
        ('f', 'follow'),
        ('b', 'block'),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_users_relation',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_users_relation',
    )
    related_type = models.CharField(
        choices=CHOICE_RELATIONS_TYPE,
        max_length=10,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
=======
    CHOICE_RELATIONS_TYPE = (('f', 'follow'), ('b', 'block'),)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_relations',
                                  related_query_name='from_users_relation')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_relations',
                                related_query_name='to_users_relation')
    related_type = models.CharField(choices=CHOICE_RELATIONS_TYPE, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> Stashed changes

    class Meta:
        unique_together = (
            ('from_user', 'to_user', 'related_type'),
            ('to_user', 'from_user', 'related_type'),
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

