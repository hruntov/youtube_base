from django.conf import settings
from django.contrib import admin
from django.db import models

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'image')
    search_fields = ('user__username',)


admin.site.register(Profile, ProfileAdmin)
