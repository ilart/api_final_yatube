from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import serializers as sz
from .permissions import IsAuthorOrReadOnly
from posts.models import Follow, Group, Post


class PostViewSet(ModelViewSet):
    serializer_class = sz.PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    serializer_class = sz.GroupSerializer
    queryset = Group.objects.all()


class FollowViewSet(ModelViewSet):
    serializer_class = sz.FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ['following__username', ]
    permission_classes = (IsAuthenticated, )

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(
            Follow,
            user=request.user.id, following__username=kwargs.get('username')
        ).delete()

    def get_queryset(self):
        return self.request.user.follower.all()


class CommentViewSet(ModelViewSet):
    serializer_class = sz.CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_queryset(self):
        return get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        ).comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return serializer.save(author=self.request.user, post=post)
