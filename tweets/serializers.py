from rest_framework import serializers
from django.conf import settings

from .models import Tweets

max_tweet_length = 240
Tweet_action_options = settings.TWEET_ACTION_LIST

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in Tweet_action_options:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweets
        fields = ['id','content','likes']
    
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > max_tweet_length:
            raise forms.ValidationError("This tweet is too long")
        return value