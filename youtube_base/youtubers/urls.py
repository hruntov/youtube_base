from django.contrib import admin
from django.urls import include, path
from youtubers import views

from .feeds import LatestYoutubersFeed
from .views import AddYoutuberView, CommentDeleteView, HomeView, YoutuberDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_youtuber/', AddYoutuberView.as_view(), name='add_youtuber'),
    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('youtuber_list/', views.YoutuberList.as_view(), name='youtuber_list'),
    path('youtuber_list/<slug:slug_name>/',
         views.YoutuberDetailView.as_view(),
         name='youtuber_detail'),
    path('youtuber/<slug:slug_name>/add_comment/', views.CommentAddView.as_view(),
         name='add_comment'),
    path('comment/<int:id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('youtuber/<slug:slug_name>/add_tag/', views.TagAddView.as_view(), name='add_tag'),
    path('feed/', LatestYoutubersFeed(), name='youtuber_feed'),
    path('search/', views.youtuber_search, name='youtuber_search'),
    path('youtuber/<int:youtuber_id>/', views.manage_subscribe, name='manage_subscribe'),
]
