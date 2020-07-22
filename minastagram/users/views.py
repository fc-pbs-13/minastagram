from django.contrib.auth import get_user_model
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.models import Profile, Relation
from users.serializers import UserSerializers, ProfileSerializer, RelationSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # permission_classes = (IsAuthenticated,)

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

    @action(detail=True)
    def follow(self, request, pk=None):
        # pk의 following
        user = get_object_or_404(User, id=pk)
        users = User.objects.filter(
            to_users_relation__from_user=user,
            to_users_relation__related_type='f'
        )
        serializer = UserSerializers(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def follower(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        users = User.objects.filter(
            from_users_relation__to_user=user,
            from_users_relation__related_type='f'
        )
        serializers = UserSerializers(users, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = (IsAuthenticated,)


class RelationViewSet(ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    # permission_classes = (IsAuthenticated,)
