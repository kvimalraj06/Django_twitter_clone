from django.db import models
from django.conf import settings # inbuild user model in django
import random

User = settings.AUTH_USER_MODEL # creating instance for user model

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) # assigned users an id,If user is deleted the tweets of that user also deleted(on_delete)
    content = models.TextField(blank=True, null=True) # to store content or text
    image = models.FileField(upload_to="image/", blank=True, null=True) # To store images


    class Meta:
        ordering = ['-id']


    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(1,100)
        }
