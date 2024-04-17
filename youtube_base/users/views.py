from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (PasswordChangeDoneView, PasswordChangeView,
                                       PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetView)
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import ContactForm, RegistrationForm


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


def contact_us(request):
    """View for handling the contact form submission. It sends an email with the form data."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            send_mail(
                'Contact Form Message',
                f'{subject}:{message}. Email:{sender}',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})


class MyPasswordChangeView(PasswordChangeView):
    """View for changing the user's password."""
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('password_change_done')


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    """View displayed after the user's password has been changed."""
    template_name = 'users/password_change_done.html'


class MyPasswordResetView(PasswordResetView):
    """View for resetting the user's password."""
    template_name = 'users/password_reset_form.html'


class MyPasswordResetDoneView(PasswordResetDoneView):
    """View displayed after the password reset email has been sent."""
    template_name = 'users/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """View for confirming the new password during a password reset."""
    template_name = 'users/password_reset_confirm.html'


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    """View displayed after the user's password has been reset."""
    template_name = 'users/password_reset_complete.html'


@login_required
def profile(request):
    return render(request, 'users/profile.html')
