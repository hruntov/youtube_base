from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

from youtubers import views
from youtubers.sitemaps import YoutuberSitemap

sitemaps = {
    "youtubers": YoutuberSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', views.TestTemplateView.as_view()),
    path('', include('youtubers.urls')),
    path('', include('users.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
