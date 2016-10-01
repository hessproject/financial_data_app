from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')