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

    def clean_email(self):
        """Validate the email field."""
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


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
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'image', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = "Дата народження"
        self.fields['image'].label = "Аватар"
        if self.instance.pk:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        """Overridden save method for the ProfileForm."""
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        if commit and self.has_changed():
            profile.save()
        return profile

    def clean_email(self):
        """Validate the email field."""
        email_data = self.cleaned_data['email']
        email = User.objects.exclude(id=self.instance.id).filter(email=email_data)
        if email.exists():
            raise forms.ValidationError('Email already in use')
        return email_data
