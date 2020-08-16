from rest_framework import serializers
from django.conf import settings

from .models import Tweets

max_tweet_length = 240

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ['content']

    def validate_content(self, value):
        if len(value) > max_tweet_length:
            raise forms.ValidationError("This tweet is too long")
        return value