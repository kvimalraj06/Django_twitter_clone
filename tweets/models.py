from django.db import models

class Tweets(models.Model):
    content = models.TextField(blank=True, null=True) # to store content or text
    image = models.FileField(upload_to="image/", blank=True, null=True) # To store images
