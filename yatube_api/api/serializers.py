from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField
from posts.models import Comment, Group, Post, Follow, User
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].username)
        if user == self.context['request'].user:
            raise serializers.ValidationError('Вы не можете подписаться')
        if Follow.objects.filter(
            user=User.objects.get(username=self.context['request'].user),
            following=User.objects.get(username=data['following'])
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписались'
            )
        return data

    class Meta:
        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('id', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            ), ]
