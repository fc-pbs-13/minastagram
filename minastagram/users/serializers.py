from rest_framework import serializers
from users.models import User, Profile, Relation


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'introduce')

    def __str__(self):
        return self.user


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('id', 'from_user', 'to_user', 'related_type')

    def perform_create(self, serializer):
        serializer.save()

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
