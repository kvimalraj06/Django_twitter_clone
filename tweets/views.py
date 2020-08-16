from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.http import is_safe_url
import random

from .models import Tweets
from .form import TweetForm
from .serializers import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Quixotic_programmer</h1>")
    return render(request, "pages/home.html")

@api_view(['POST'])# list of methods that need to support
@authentication_classes([SessionAuthentication]) # having valid session or not
@permission_classes([IsAuthenticated]) # only the user is authenticated it allows to access below view
def tweet_create_view(request, *args, **kwargs):
    """Using rest_framework"""
    serializer = TweetSerializer(data = request.POST or None) # instance for serializer
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user) # saving the tweet to particular user
    serialized_data_with_likes = {**serializer.data, **{"likes":random.randint(0,100)}}
    return Response(serialized_data_with_likes, status=201)# created items

@api_view(["GET"])
def list_view(request, *args, **kwargs):
    qs = Tweets.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def tweet_detailed_view(request, tweet_id, *args, **kwargs):
    qs = Tweets.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status = 200)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweets.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    qs = qs.filter(user = request.user)
    if not qs.exists():
        return Response({"message":"You can't Delete the tweet"}, status = 401)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet Deleted"}, status = 200)

def tweet_create_view_pure_django(request, *args, **kwargs):
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

def list_view_pure_django(request, *args, **kwargs):
    qs = Tweets.objects.all()
    tweet_list = [x.serialize() for x in qs]
    tweet_list.reverse()
    data = {
        "response" : tweet_list
    }
    return JsonResponse(data)


def tweet_detailed_view_pure_django(request, tweet_id, *args, **kwargs):
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

