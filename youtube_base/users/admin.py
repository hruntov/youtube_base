from django.contrib import admin

from .models import Profile


from django.conf import settings
from django.db import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'image')
    search_fields = ('user__username',)


admin.site.register(Profile, ProfileAdmin)
