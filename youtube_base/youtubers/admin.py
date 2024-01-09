from django.contrib import admin

from .models import Video, Youtuber

admin.site.register(Youtuber)
admin.site.register(Video)
