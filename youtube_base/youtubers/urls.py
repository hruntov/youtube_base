from django.contrib import admin
from django.urls import include, path

from youtubers import views

from .views import AddYoutuberView, HomeView, YoutuberDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_youtuber/', AddYoutuberView.as_view(), name='add_youtuber'),
    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('youtuber_list/', views.YoutuberList.as_view(), name='youtuber_list'),
    path('youtuber_list/<slug:slug>/',
         views.YoutuberDetailView.as_view(),
         name='youtuber_detail'),
]
