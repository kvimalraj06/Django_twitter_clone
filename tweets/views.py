from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Tweets

def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Quixotic_programmer</h1>")
    return render(request, "pages/home.html")

def list_view(request, *args, **kwargs):
    qs = Tweets.objects.all()
    tweet_list = [{"id":x.id, "content": x.content} for x in qs]
    data = {
        "tempted": "true",
        "response" : tweet_list
    }
    return JsonResponse(data)


def tweet_detailed_view(request, tweet_id, *args, **kwargs):
    """Rest API view example"""
    data = {
        "id": tweet_id,
    }
    
    status = 200

    try:
        obj = Tweets.objects.get(id=tweet_id)
        data["content"] = obj.content

    except:
        data["content"] = "not found"
        status =  404
    
    return JsonResponse(data, status = status) # to return the data in json format

