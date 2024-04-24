from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(UserCreationForm):
    """A form for registering a new user."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2')


class ContactForm(forms.Form):
    """A form for contacting the site administrators."""
    subject = forms.CharField(max_length=200, label='Тема')
    message = forms.CharField(widget=forms.Textarea, label='Повідомлення')
    sender = forms.EmailField(label='Ваша електронна адреса')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(name='submit', value='Відправити'))


class ProfileForm(forms.ModelForm):
    """A Django form for the Profile model."""
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = "Дата народження"
        self.fields['image'].label = "Аватар"
