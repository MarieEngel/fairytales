from django import forms
from django.forms import ModelForm

from .models import Fairytale


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=50, widget=forms.PasswordInput
    )  # hides the input


class AddFairytaleForm(ModelForm):
    class Meta:
        model = Fairytale
        fields = ["title", "author", "image", "body", "slug"]


class SearchForm(forms.Form):
    query = forms.CharField(label="Search term", max_length=50)
