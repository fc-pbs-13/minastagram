from django.db.models import Q
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer, RecursiveSerializer, PostProfileSerializers
from users.models import User

"""
cmd + fc + F8  : break point
cmd + 2 : break point 위치 확인
"""


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # permission_classes = (IsAuthenticated,)
    def perform_create(self, serializer):
        # serializer 를 저장을 할 건데

        serializer.save(context={'request_user': self.request.user})

    @action(detail=True, methods=['post'])
    def like_toggle(self, request, pk=None):
        """
        :param request:
        :param pk: post pk
        :return: status code
        """
        post = get_object_or_404(Post, id=pk)

        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            post.like_users.add(request.user)
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=False)
    def page(self, request):
        # 내가 팔로우를 건 유저들의 게시글 User.objects.filter(
        # 1.내가 from_user인 릴레이션 중 팔로우인 것
        # OR
        # 2.피케이가 나인 것
        qs = User.objects.filter(
            Q(to_users_relation__from_user=request.user,to_users_relation__related_type='f') |
            Q(pk=request.user.pk)
        ).values_list('id').distinct()
        posts = Post.objects.filter(owner__id__in=qs)
        # context 를 넣는 경우는 생성 , 업데이트 외에 쓸 일이 없다.
        serializers = PostProfileSerializers(posts, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # permission_classes = (IsAuthenticated,)

    # 하드코딩
    def perform_create(self, serializer):
        if 'comment_pk' in self.kwargs:
            comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
            serializer.save(
                author=self.request.user,
                parent=comment
            )
        elif 'post_pk' in self.kwargs:
            post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
            serializer.save(
                author=self.request.user,
                post=post
            )
        else:
            raise serializers.ValidationError('대댓글만 작성 가능')
