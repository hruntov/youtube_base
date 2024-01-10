from django.contrib import admin

from .models import Category, Video, Youtuber

admin.site.register(Youtuber)
admin.site.register(Video)
admin.site.register(Category)
