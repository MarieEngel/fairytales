from django import forms
from django.forms import HiddenInput, ModelForm

from .models import Fairytale, Profile, Category, Comment


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
   

# class AddFairytaleForm(ModelForm):
#     class Meta:
#         model = Fairytale
#         fields = ["title", "author", "image", "body", "slug", "posted_by"]
#         widgets = {
#             "posted_by": HiddenInput()
#         }


choices = Category.objects.all().values_list(
    "name", "name"
)  # alternative for hard coding
choice_list = []

for item in choices:
    choice_list.append(item)


class AddFairytaleForm(ModelForm):
    class Meta:
        model = Fairytale
        exclude = ["posted_by", "vector_column"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "image":forms.FileInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(
                choices=choice_list, attrs={"class": "form-control"}
            )
        }


class SearchForm(forms.Form):
    query = forms.CharField(label="Search term", max_length=50)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "prefered_settings", "image"]


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["fairytale"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"})}
