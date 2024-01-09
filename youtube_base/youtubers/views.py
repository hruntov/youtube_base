from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from youtube_api.add_youtuber import YoutubeApi

from . import models
from .forms import AddYoutuberForm
from .models import Youtuber


class TestTemplateView(TemplateView):
    template_name = "youtubers/test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_data'] = models.TestModel.objects.all()
        return context


class HomeView(TemplateView):
    template_name = "youtubers/home.html"

    def home(request):
        return render(request, 'youtubers/home.html')


class AddYoutuberView(FormView):
    template_name = 'youtubers/add_youtuber.html'
    form_class = AddYoutuberForm
    success_url = reverse_lazy('add_youtuber')

    def form_valid(self, form):
        url = form.cleaned_data['url']
        youtube_channel = YoutubeApi(url)
        youtube_channel.get_channel_data()

        youtuber = Youtuber(
            channel_id=youtube_channel.channel_id,
            channel_title=youtube_channel.channel_title,
            username=youtube_channel.username,
            channel_description=youtube_channel.channel_description,
            youtube=youtube_channel.channel_url,
            slug_name=slugify(youtube_channel.username)
        )
        youtuber.save()

        return super().form_valid(form)
