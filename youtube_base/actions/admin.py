from django.contrib import admin
from youtube_base.actions.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'target', 'created']
    list_filter = ['created']
    search_fields = ['action']
