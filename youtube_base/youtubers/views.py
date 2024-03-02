from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView
from taggit.models import Tag

from youtube_api.add_youtuber import YoutubeApi

from . import models
from .forms import AddYoutuberForm, CategoryForm, CommentForm, TagForm
from .models import Category, Comment, Youtuber
from .serialaizer import YoutuberSerializer


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
        model(Model): The model class to use for the ListView.
        template_name (str): The template to use for rendering the view.
        context_object_name (str): The name of the variable to use for the list of categories in the
            template context.

    """
    model = Category
    template_name = 'youtubers/category_list.html'
    context_object_name = 'categories'


class YoutuberList(ListView):
    """
    A ListView that displays a list of Youtubers from chosen categories.

    Attributes:
        model (Model): The model that this view displays. Set to the Youtuber model.

    """
    model = Youtuber
    paginate_by = 3
    template_name = 'youtubers/youtuber_list.html'

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        tag_form = TagForm(request.POST)

        if form.is_valid():
            categories = form.cleaned_data['categories']
            youtubers = Youtuber.objects.filter(categories__in=categories)
        elif tag_form.is_valid():
            tag = tag_form.cleaned_data['tag']
            youtubers = Youtuber.objects.filter(tags__name__in=[tag])
        else:
            messages.error(request, 'Будь-ласка оберіть хоча б одну категорію.')
            return redirect('home')

        return self.render_youtubers(request, youtubers)

    def render_youtubers(self, request, youtubers):
        """
        Renders the 'youtubers/youtuber_list.html' template with the provided list of Youtubers.

        Args:
            request (HttpRequest): The request instance.
            youtubers (QuerySet): The list of Youtubers to display.

        Returns:
            (HttpResponse): The response instance. A rendered template with the paginated list of
                Youtubers.

        """
        page = request.POST.get('page', 1)
        youtubers_paginated = self._get_paginated_data(youtubers, page)

        serializer = YoutuberSerializer(youtubers, many=True)
        youtubers = serializer.data
        request.session["youtubers"] = youtubers

        return render(request,
                      'youtubers/youtuber_list.html',
                      {'youtubers': youtubers_paginated})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the YoutuberList view.

        This method retrieves the list of Youtubers from the session that was stored during the POST
        request. It then renders the 'youtubers/youtuber_list.html' template with the list of Youtubers.

        Args:
            request (HttpRequest): The request instance.

        Returns:
            (HttpResponse): The response instance. A rendered template with the list of Youtubers.

        """
        page = request.GET.get('page', 1)
        youtubers = request.session.get("youtubers", [])
        youtubers_paginated = self._get_paginated_data(youtubers, page)
        return render(request, self.template_name, {'youtubers': youtubers_paginated})

    def _get_paginated_data(self, data, page):
        """
        This function creates a Paginator instance with the provided data and page size. It then
        gets the current page number from the request's GET parameters and retrieves the Page
        instance for that page number.

        Args:
            request (HttpRequest): The request instance.
            data (QuerySet): The data to be paginated.
            page_size (int): The number of items per page.

        Returns:
            page (Page): The Page instance for the current page number. Contains the items for the
                current page, as well as pagination information (e.g., whether there are
                previous/next pages).

        """
        paginator = Paginator(data, self.paginate_by)
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)
        return paginated_data

    def pagination(self, request, youtubers):
        page = request.POST.get('page', 1)
        youtubers_paginated = self._get_paginated_data(youtubers, page)

        serializer = YoutuberSerializer(youtubers, many=True)
        youtubers = serializer.data

    def session(self, request, youtubers):
        request.session["youtubers"] = youtubers


class YoutuberDetailView(DetailView):
    """A DetailView for displaying details of a Youtuber.

    Attributes:
        model (Model): The model that this view displays. In this case, it's the Youtuber model.
        slug_field (str): The field that's used for search the Youtuber. In this case, it's
            'slug_name'.
        template_name (str): The template used for displaying the Youtuber. In this case, it's
            'youtubers/youtuber_detail.html'.

    """
    model = Youtuber
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'youtubers/youtuber_detail.html'

    def get_context_data(self, **kwargs):
        """
        Overridden method from Django's DetailView to modify the context data.

        This method retrieves the default context data from the superclass's method,
        then changes the key from 'object' to 'youtuber' for clarity in the template.

        Returns:
            context (dict): The modified context data.

        """
        context = super().get_context_data(**kwargs)
        context['youtuber'] = context.pop('object')
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(youtuber=context['youtuber']).order_by('-created_at')[:5]
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for the YoutuberDetailView. This method validates the submitted form
        and saves the comment to the database.

        Args:
            request (HttpRequest): The request instance.

        Returns:
            (HttpResponse): The response instance. Either a redirect to the same page with the new
                comment, or a redirect to the same page with an error message.

        """
        youtuber = get_object_or_404(Youtuber, slug_name=kwargs.get('slug_name'))
        form = CommentForm(data=request.POST)
        if not request.user.is_authenticated:
            messages.error(request, 'Будь-ласка увійдіть, щоб залишити коментар.')
            return redirect('youtuber_detail', slug_name=youtuber.slug_name)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.youtuber = youtuber
            comment.user = request.user
            comment.save()
            return redirect('youtuber_detail', slug_name=youtuber.slug_name)
        else:
            messages.error(request, 'Будь-ласка введіть коректний коментар.')
            return redirect('youtuber_detail', slug_name=youtuber.slug_name)


class CommentDeleteView(View):
    """A View for deleting comments."""
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('id'))
        if request.user == comment.user:
            comment.delete()
            messages.success(request, 'Коментар видалено.')
        else:
            messages.error(request, 'Ви не можете видалити цей коментар.')
        return redirect('youtuber_detail', slug_name=comment.youtuber.slug_name)
