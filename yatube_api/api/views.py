from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Group, Post, Follow
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .serializers import FollowSerializer
from .permissions import AuthorPermission
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorPermission,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorPermission,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorPermission, ]
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['user', 'following', ]

    def get_queryset(self):
        queryset = Follow.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
