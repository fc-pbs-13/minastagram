from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# 어떤 값이 들어올지 모름
# *args = 함수에 변수가 튜플형태로 입력 a(1,2,3,4,) => (1,2,3,4)
# **kwargs = 딕셔너리 형태로 입력 b(a=1, b=2, c=3) => { a:1, b:2, c:3}
from django.db.models import F
from rest_framework.generics import get_object_or_404


class User(AbstractUser):
    # 32비트 정수형 필드
    follow = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        is_created = self.id is None
        # None?
        user = super().save()

        if is_created:
            Profile.objects.create(user=self)

        return user

    @property  # get 메서드를 표현 = @property / set 메서드를 표현 = @method_name.setter
    def follow(self):
        # 내가 팔로우를 건 유저
        user = User.objects.filter(to_users_relation__from_user=self, to_users_relation__related_type='f')
        return user

    @property
    def follower(self):
        # 나를 팔로우를 건 유저
        user = User.objects.filter(from_users_relation__to_user=self, from_users_relation__related_type='f')
        return user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    nickname = models.CharField(max_length=15, )
    introduce = models.CharField(max_length=100, null=True, )
    follow_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)


class Relation(models.Model):
    class choice_relations_type(models.TextChoices):
        FOLLOW = 'f', _('Follow')
        BLOCK = 'b', _('Block')
        """
        .labels ->> 외부에 보여지는 값 // ['Follow', 'Block'] 
        .values ->> 데이터베이스에 저장 되는 값.// ['f', 'b']
        .choices ->> 라벨, 벨류 값 같이 // [('f', 'Follow'), ('b', 'Block')]
        .names ->> 클래스 변수 값 // ['FOLLOW', 'BLOCK']
        """

    # CHOICE_RELATIONS_TYPE = (('f', 'follow'), ('b', 'block'))
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_relations',
                                  related_query_name='from_users_relation')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_relations',
                                related_query_name='to_users_relation')
    related_type = models.CharField(choices=
                                    choice_relations_type.choices,
                                    # CHOICE_RELATIONS_TYPE,
                                    max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user', 'related_type'),
            ('to_user', 'from_user', 'related_type'),
        )

    def save(self, *args, **kwargs):
        # from_user = get_object_or_404(User, pk=self.from_user_id)
        # to_user = get_object_or_404(User, pk=self.to_user_id)

        created = self.id is None

        super().save(*args, **kwargs)

        if created and self.related_type == 'f':
            # 팔로우를 건 유저의 팔로윙 카운트 증가.
            self.from_user.profile.follow_count = F('follow_count') + 1
            self.to_user.profile.follower_count = F('follower_count') + 1
            self.from_user.profile.save()
            self.to_user.profile.save()

        elif created is False and self.related_type == 'b':
            # 팔로우를 건 유저의 팔로윙 카운트 증가
            self.from_user.profile.follow_count = F('follow_count') - 1
            self.to_user.profile.follower_count = F('follower_count') - 1
            self.from_user.profile.save()
            self.to_user.profile.save()

    def delete(self, *args, **kwargs):
        # from_user = get_object_or_404(User, pk=self.from_user_id)
        # to_user = get_object_or_404(User, pk=self.to_user_id)

        super().delete(*args, **kwargs)

        if self.related_type == 'f':
            # 팔로우를 건 유저의 팔로윙 카운트 증가.
            self.from_user.profile.follow_count = F('follow_count') - 1
            self.to_user.profile.follower_count = F('follower_count') - 1
            self.from_user.profile.save()
            self.to_user.profile.save()
