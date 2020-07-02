import serializers as serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['username'],
            password=validated_data['password'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
