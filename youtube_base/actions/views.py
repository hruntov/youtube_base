from django.shortcuts import render
from youtube_base.actions.models import Action


def dashboard(request):
    """Render the dashboard page with the latest 10 actions excluding the current user."""
    actions = Action.objects.exclude(user=request.user)[:10]
    return render(request,'actions/dashboard.html', {'sections': 'dashboard',
                                                     'actions': actions})
