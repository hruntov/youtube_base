from django import forms
from .models import Youtuber


class AddYoutuberForm(forms.ModelForm):
    """
    A Django form used to create a new Youtuber instance. The 'categories' field allowing multiple
    categories to be selected.

    """
    class Meta:
        model = Youtuber
        fields = ['youtube_url', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }
