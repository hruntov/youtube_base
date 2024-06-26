from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from users import views

urlpatterns = [
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.MyPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', views.MyPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete', views.MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('profile', views.profile, name='profile'),
    path('social-auth/', include('social_django.urls', namespace='social')),

]
