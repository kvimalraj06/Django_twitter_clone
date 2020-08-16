from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
import random

from .models import Tweets
from .form import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    print(request.user)
    #return HttpResponse("<h1>Quixotic_programmer</h1>")
    return render(request, "pages/home.html")

def tweet_create_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit = False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201) # created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
           return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status = 400)
    return render(request, "Components/form.html", context={'form': form})

def list_view(request, *args, **kwargs):
    qs = Tweets.objects.all()
    tweet_list = [x.serialize() for x in qs]
    tweet_list.reverse()
    data = {
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

