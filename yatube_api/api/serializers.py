from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from posts.models import Comment, Follow, Group, Post

SELF_FOLLOW_FORBIDDEN = 'Подписка на самогосебя запрещена.'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        try:
            data['following'] = User.objects.get(username=data['following'])
        except ObjectDoesNotExist as error:
            raise serializers.ValidationError(error)
        data['user'] = self.context['request'].user
        if data['following'] == data['user']:
            raise serializers.ValidationError(SELF_FOLLOW_FORBIDDEN)
        return data

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post', )
