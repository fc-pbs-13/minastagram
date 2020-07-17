from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer, RecursiveSerializer
from users.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # 하드코딩
    def perform_create(self, serializer):
        if 'comment_pk' in self.kwargs:
            comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
            serializer.save(
                # author=self.request.user,
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
