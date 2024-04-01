import os
import markdown
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Youtuber


class LatestYoutubersFeed(Feed):
    """A Feed class that generates an RSS feed for the latest Youtubers."""
    title = 'Українська база ютуберів.'
    desription = 'Новий ютубер у нашій базі.'

    def items(self):
        """Return the Youtuber objects that should be included in the feed."""
        return Youtuber.objects.all()[:5]

    def update_site_info(self):
        """Update the current site's domain and name."""
        site = Site.objects.get_current()
        site.domain = os.environ.get('SITE_DOMAIN')
        site.name = os.environ.get('SITE_NAME')
        site.save()

    def link(self, item):
        """Return the URL for the feed itself."""
        self.update_site_info()

        domain = Site.objects.get_current().domain
        link_list = 'http://' + domain + reverse_lazy('youtuber_list')
        return link_list

    def item_link(self, item):
        """Return the URL for an individual item in the feed."""
        domain = Site.objects.get_current().domain
        item_link = 'http://' + domain + reverse_lazy('youtuber_detail', args=[item.slug_name])
        return item_link

    def item_title(self, item):
        """Return the title for an individual item in the feed."""
        return item.channel_title

    def item_description(self, item):
        """Return the description for an individual item in the feed."""
        description = truncatewords_html(markdown.markdown(item.channel_description), 30)
        category_names = ", ".join(category.name for category in item.categories.all())
        return f"Categories: {category_names}\n{description}"

    def item_pubdate(self, item):
        """Return the publication date for an individual item in the feed."""
        return item.created_at
