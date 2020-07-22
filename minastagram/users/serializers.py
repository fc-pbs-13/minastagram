from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from users.models import User, Profile, Relation


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        # 필드에 임의의 추가 키워드 인수를 지정할 수 있는 단축키. serializer에서 필드를 명시적으로 선언 할 필요가 없음을 의미

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'introduce', 'follow_count', 'follower_count')

    def __str__(self):
        return self.user


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('id', 'from_user', 'to_user', 'related_type')

    # def validate_from_user(self, from_user):
    #     # if not User.objects.filter(id=from_user).exists():
    #     #     raise serializers.ValidationError()
    #
    #     get_object_or_404(User, pk=self.from_user)
    #
    #     return from_user
    #
    # def validate_to_user(self, to_user):
    #     get_object_or_404(User, pk=self.to_user)
    #
    #     return to_user
