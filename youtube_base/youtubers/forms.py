from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from .models import Category, Comment, Youtuber


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


class CategoryForm(forms.Form):
    """
    A form for selecting categories.

    This form provides a multiple selection checkbox field for categories. The field is not required,
    meaning the form can be submitted without selecting any categories.

    Attributes:
        categories (forms.ModelMultipleChoiceField): A multiple choice field for selecting categories.
            The choices for this field are populated with all Category instances. The field uses a
            CheckboxSelectMultiple widget, allowing multiple categories to be selected at once.
    """
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean(self):
        """
        Validates the form data.

        This method is called after the form's built-in validation. It checks if at least one
        category has been selected. If no categories have been selected, it raises a
        ValidationError.

        Raises:
            forms.ValidationError: If no categories have been selected.

        """
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')

        if not categories:
            raise forms.ValidationError("")


class CommentForm(forms.ModelForm):
    """
    A Django form used for creating a new Comment instance.

    Attributes:
        text (forms.CharField): A field for entering the comment text.

    """
    text = forms.CharField(widget=forms.Textarea, label='Комментар')

    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(name='submit', value='Відправити'))


class TagForm(forms.Form):
    """
    A form used for filtering Youtubers by tag. If the form is filled out, the tag inputted is used
    to filter the Youtubers displayed in the view.

    Attributes:
        tag (forms.CharField): A character field for inputting a tag.

    """
    tag = forms.CharField(max_length=255)


class SearchForm(forms.Form):
    """
    A Django form used for searching Youtubers.

    Attributes:
        query (forms.CharField): A character field for inputting a search query.

    """
    query = forms.CharField(label='Ваш запит')
