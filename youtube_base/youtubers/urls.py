from django.contrib import admin
from django.urls import include, path
from youtubers import views

from .views import HomeView as home

urlpatterns = [
    path('', home.home)
]