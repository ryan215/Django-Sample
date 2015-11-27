from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from workouts.models import Video, VideoComment
from django.db.models import F
from django.contrib.auth import get_user_model
from notifications import notify
User = get_user_model()



# for typeahead on workouts search
class TitleSerializer(serializers.ModelSerializer):
    def to_native(self, obj):
        return {"name": obj.title}

    class Meta:
        model = Video

    fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    img = serializers.CharField(source='user.img.url', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    class Meta:
        model = VideoComment


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class VideoLikeSerializer(serializers.ModelSerializer):
    user_pk = serializers.CharField(max_length=50)

    class Meta:
        model = Video
        fields = ('id', "user_pk",)

    def to_native(self, value):
        obj = super(VideoLikeSerializer, self).to_native(value)
        user = User.objects.get(id=obj['user_pk'])
        if value.likes_user.filter(pk=user.pk).exists():
            obj['user_likes'] = False
            value.likes_user.remove(user)
        else:
            obj['user_likes'] = True
            value.likes_user.add(user)
            # if User.objects.filter(id = value.user_id).exists():
            #     notify.send(user, recipient=value.user, verb=u'liked your video!')
        return obj

    def validate_user_email(self, attrs, source):
        if User.objects.filter(id=attrs['user_pk']).exists():
            pass
        else:
            raise serializers.ValidationError("User must exist to like content")
        return attrs


class VideoSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(allow_empty_file=True, required=False)
    likes = serializers.Field(source="likes_user.count")

    class Meta:
        model = Video

    def to_native(self, value):
        obj = super(VideoSerializer, self).to_native(value)
        # In order to keep views on point, using F class to keep track
        value.views = F('views') + 1
        value.save()
        # check if user likes the video
        user = self.context['request'].user
        obj['user_likes'] = value.likes_user.filter(pk=user.pk).exists()
        return obj


class VideoCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Video
        fields = ('comments',)

