from django import forms

from .models import Tweets

max_tweet_length = 200


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get("content")
        stripped_content = content.strip()
        if len(content) > max_tweet_length:
            raise forms.ValidationError("This tweet is too long")
        elif content == "" or stripped_content == "":
            raise forms.ValidationError("The tweet should not be empty")
        return content