from django.contrib import admin
from .models import Tweets, TweetLike

# Register your models here.
class TweeetLikeadmin(admin.TabularInline):
    model = TweetLike

class TweetAdmin(admin.ModelAdmin):
    inlines = [TweeetLikeadmin]
    list_display = ["__str__", "user", "id", "content"]
    search_fields = ["user__username"]
    class Meta:
        model = Tweets


admin.site.register(Tweets, TweetAdmin)