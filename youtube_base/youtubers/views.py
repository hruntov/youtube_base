from django.shortcuts import render
from django.views.generic import TemplateView

from . import models


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
