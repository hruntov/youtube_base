from django.db import models


class Youtuber(models.Model):
    """The Youtuber model represents a YouTube channel.

    Attributes:
        id: The primary key of the Youtuber.
        channel_id: The ID of the YouTube channel.
        channel_title: The title of the YouTube channel.
        username: The username of the Youtuber.
        channel_description: The description of the YouTube channel.
        created_at: The date and time when the Youtuber was added.
        updated_at: The date and time when the Youtuber was last updated.
        youtube_url: The URL of the YouTube channel.
        twitch_url: The URL of the Youtuber's Twitch channel.
        telegram_url: The URL of the Youtuber's Telegram channel.
        instagram_url: The URL of the Youtuber's Instagram page.
        facebook_url: The URL of the Youtuber's Facebook page.
        slug_name: The slugified version of the Youtuber's username.
        categories: The categories that the Youtuber belongs to. This is a many-to-many field
            referencing the Category model.

    """
    id = models.AutoField(primary_key=True)
    channel_id = models.CharField(max_length=100)
    channel_title = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    channel_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    youtube_url = models.CharField(max_length=100, blank=True, null=True)
    twitch_url = models.CharField(max_length=100, blank=True, null=True)
    telegram_url = models.CharField(max_length=100, blank=True, null=True)
    instagram_url = models.CharField(max_length=100, blank=True, null=True)
    facebook_url = models.CharField(max_length=100, blank=True, null=True)
    slug_name = models.SlugField(max_length=100, blank=True, null=True)
    categories = models.ManyToManyField('Category', related_name='youtubers')

    def __str__(self):
        return self.channel_title

    class Meta:
        verbose_name_plural = "Youtubers"
        ordering = ['id']


class Video(models.Model):
    """The Video model represents a video posted by a Youtuber.

    Attributes:
        id: The primary key of the Video.
        title  The title of the video.
        url: The URL of the video.
        youtuber: The Youtuber who posted the video. The foreign key referencing the Youtuber model.
        slug_name: The slugified version of the video's title.

    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    youtuber = models.ForeignKey('Youtuber', on_delete=models.CASCADE, related_name='videos')
    slug_name = models.SlugField(max_length=255, blank=True, null=True)


class Category(models.Model):
    """
    The CategoryYoutuber model represents a category that a Youtuber can belong to.

    Attributes:
        id: The primary key of the Category.
        name: The name of the category.
        description: A description of the category.

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
