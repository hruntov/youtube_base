from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def sign_up_view(request):
    """
    View for user registration.

    If the request method is POST, it tries to validate the form and save the new user.
    If the form is valid, it logs in the new user and redirects to the home page.
    If the form is not valid, it re-renders the registration page with the form errors.
    If the request method is not POST (i.e., GET), it displays an empty registration form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        (HttpResponse): The response object.

    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})


def logout_view(request):
    """
    View for user logout. It logs out the user and redirects to the home page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        (HttpResponse): The response object.

    """
    logout(request)
    return redirect('/')
