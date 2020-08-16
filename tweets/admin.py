from django.contrib import admin
from .models import Tweets

# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "id", "content"]
    search_fields = ["user__username"]
    class Meta:
        model = Tweets


admin.site.register(Tweets, TweetAdmin)