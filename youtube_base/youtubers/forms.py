from django import forms

from .models import Category, Youtuber


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
