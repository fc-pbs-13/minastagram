from django.conf.urls import url
from django.urls import path, include
from rest_framework_nested import routers
from posts.views import PostViewSet, CommentViewSet
from users.views import UserViewSet, ProfileViewSet, RelationViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'comments', CommentViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostViewSet)
users_router.register(r'profile', ProfileViewSet)
users_router.register(r'relation', RelationViewSet)


posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet)

comment_router = routers.NestedSimpleRouter(router, r'comments', lookup='comment')
comment_router.register(r'reply', CommentViewSet)


urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
    url(r'^', include(posts_router.urls)),
    url(r'^', include(comment_router.urls)),
)
