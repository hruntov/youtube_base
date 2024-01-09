from django import forms


class AddYoutuberForm(forms.Form):
    url = forms.URLField(label='URL of the Youtuber')
