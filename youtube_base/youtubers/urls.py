from django.contrib import admin
from django.urls import path
from youtubers import views
from django.urls import include
from .views import HomeView as home


urlpatterns = [
    path('', home.home)
]