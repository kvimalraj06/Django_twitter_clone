from django.db import models
from django.conf import settings # inbuild user model in django
import random

User = settings.AUTH_USER_MODEL # creating instance for user model

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tweet = models.ForeignKey('Tweets', on_delete = models.CASCADE) # for below tweets modele
    timestamp = models.DateTimeField(auto_now_add=True) # adding time of liking

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) # assigned users an id,If user is deleted the tweets of that user also deleted(on_delete)
    content = models.TextField(blank=True, null=True) # to store content or text
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)# Creating like field
    timestamp = models.DateTimeField(auto_now_add=True) # adding time of liking
    image = models.FileField(upload_to="image/", blank=True, null=True) # To store images


    class Meta:
        ordering = ['-id']


    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(1,100)
        }
