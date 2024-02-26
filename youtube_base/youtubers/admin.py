from django.contrib import admin

from .models import Category, Comment, Video, Youtuber


class YoutuberAdmin(admin.ModelAdmin):
    """The YoutuberAdmin class defines the admin interface for the Youtuber model."""
    list_display = ('id',
                    'channel_id',
                    'channel_title',
                    'username', 'youtube_url',
                    'get_categories',
                    'slug_name')

    def get_categories(self, obj):
        """
        Returns a string of all the category names associated with a Youtuber.

        Args:
            obj (Youtuber): The Youtuber instance.

        Returns:
            (str): A string of category names.
        """
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    """The CategoryAdmin class defines the admin interface for the Category model."""
    list_display = ('id',
                    'name',
                    'description')


class CommentAdmin(admin.ModelAdmin):
    """The CommentAdmin class defines the admin interface for the Comment model."""
    list_display = ('name',
                    'text',
                    'youtuber',
                    'created_at')
    list_filter = ('created_at',
                   'updated_at')
    search_fields = ('name',
                     'text')


admin.site.register(Youtuber, YoutuberAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Video)
admin.site.register(Comment, CommentAdmin)
