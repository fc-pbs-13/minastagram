from django.contrib.auth import get_user_model
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.models import Profile, Relation
from users.serializers import UserSerializers, ProfileSerializer, RelationSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = User.objects.get(username=request.data.get('username'))
        if user.check_password(request.data.get('password')):
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        user = request.user
        user.auth_token.delete()
        data = {
            "logout!!!!!"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def follow(self, request):
        # 내가 팔로우를 건 유저
        # users = request.user.follow
        # user = User.objects.first()
        users = User.objects.filter(
            to_users_relation__from_user=self.request.user,
            to_users_relation__related_type='f'
        )

        serializer = UserSerializers(users, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def follower(self, request):
        users = request.user.follower
        serializers = UserSerializers(users, many=True, )
        return Response(serializers.data, status=status.HTTP_200_OK)


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RelationViewSet(ModelViewSet):
    """
     user간의 릴레이션을 만들어야 한다.
     /relation/

     /user/1/relation >> 특정 유저의가 팔로윙 팔로워를 to user- 미나님
     request.user > 영훈

   """
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
