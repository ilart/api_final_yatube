from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (CommentSerializer, GroupSerializer,
                          FollowSerializer, PostSerializer)
from .permissions import IsAuthorOrReadOnly
from posts.models import Group, Post


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ['following__username', ]
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_post(self):
        return get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        return serializer.save(author=self.request.user, post=post)
