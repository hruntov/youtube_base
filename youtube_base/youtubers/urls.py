from django.contrib import admin
from django.urls import include, path
from youtubers import views

from .views import AddYoutuberView
from .views import HomeView as home

urlpatterns = [
    path('', home.home),
    path('add_youtuber/', AddYoutuberView.as_view(), name='add_youtuber'),
]