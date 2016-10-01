from django import forms
from stocks.models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text='Please enter category name')
    url = forms.URLField(help_text='Enter the API Endpoint')

    class Meta:
        model = Category
        fields = ('name','url')
