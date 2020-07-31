from django.shortcuts import render
from django.http import HttpResponse

from .models import Tweets

def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Quixotic_programmer</h1>")

def tweet_detailed_view(request, tweet_id, *args, **kwargs):
    obj = Tweets.objects.get(id=tweet_id)
    return HttpResponse(f"<h1>Quixotic_programmer's {obj.content} </h1>")

