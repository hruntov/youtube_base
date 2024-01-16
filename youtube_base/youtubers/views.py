from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from youtube_api.add_youtuber import YoutubeApi

from . import models
from .forms import AddYoutuberForm
from .models import Category, Youtuber


class TestTemplateView(TemplateView):
    template_name = "youtubers/test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_data'] = models.TestModel.objects.all()
        return context


class BaseCategoryMixin:
    """
    Mixin for views displaying categories.

    This mixin provides a method to include categories in the context of a view. Categories are
    retrieved from the cache, and if not present, they are fetched from the database and stored in
    the cache.

    """
    def get_context_data(self, **kwargs):
        """Enhances the context with category data.

        Returns:
            (dict): The context data.

        """
        context = super().get_context_data(**kwargs)
        categories = cache.get('all_categories')

        if categories is None:
            categories = list(Category.objects.all())
            cache.set('all_categories', categories)

        context['categories'] = categories
        return context


class HomeView(BaseCategoryMixin, TemplateView):
    """TemplateView for displaying the home page.

    Attributes:
        template_name (str): The template to use for rendering the view.

    """
    template_name = "youtubers/home.html"

    def setup(self, request, *args, **kwargs):
        """
        Additional setup logic for the view.

        Ensures that the context data, including categories, is prepared before rendering the
            template.

        Args:
            (request): The HTTP request object.

        """
        super().setup(request, *args, **kwargs)
        self.get_context_data()


class AddYoutuberView(FormView):
    template_name = 'youtubers/add_youtuber.html'
    form_class = AddYoutuberForm
    success_url = reverse_lazy('add_youtuber')

    def form_valid(self, form):
        url = form.cleaned_data['youtube_url']
        categories = form.cleaned_data['categories']
        youtube_channel = YoutubeApi(url)
        youtube_channel.get_channel_data()

        youtuber = Youtuber(
            channel_id=youtube_channel.channel_id,
            channel_title=youtube_channel.channel_title,
            username=youtube_channel.username,
            channel_description=youtube_channel.channel_description,
            youtube_url=youtube_channel.channel_url,
            slug_name=slugify(youtube_channel.username)
        )
        youtuber.save()
        youtuber.categories.set(categories)

        return super().form_valid(form)


class CategoryList(BaseCategoryMixin, ListView):
    """ListView for displaying a list of categories.

    Attributes:
        model(Category): The model class to use for the ListView.
        template_name (str): The template to use for rendering the view.
        context_object_name (str): The name of the variable to use for the list of categories in the
            template context.

    """
    model = Category
    template_name = 'youtubers/category_list.html'
    context_object_name = 'categories'
