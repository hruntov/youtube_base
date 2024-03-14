from django.contrib.sitemaps import Sitemap
from .models import Youtuber


class YoutuberSitemap(Sitemap):
    """A Django sitemap for the Youtuber model.

    Attributes:
        changefreq (str): The frequency with which the content of the page is likely to change.
        priority (float): The priority of this URL relative to other URLs on your site.

    """
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """Returns a QuerySet of all Youtuber objects."""
        return Youtuber.objects.all()

    def lastmod(self, obj):
        """Returns the date when the Youtuber object was last modified"""
        return obj.updated_at
