from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),    # The 'login/' path is included here
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact_us/', views.contact_us, name='contact_us')
]
