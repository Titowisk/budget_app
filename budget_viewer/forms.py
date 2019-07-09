from django import forms
from bank_statements_reader.models import Category

# Django Form Fields
# https://docs.djangoproject.com/en/2.2/ref/forms/fields/

class CategoryForm(forms.Form):

    category = forms.ChoiceField(choices=Category.TRANSLATION_PTBR)

    # https://docs.djangoproject.com/en/2.2/ref/forms/widgets/#styling-widget-instances
    category.widget.attrs.update({'class': 'custom-select', 'id': 'edit-category-select'}) # add bootstrap class to <select>