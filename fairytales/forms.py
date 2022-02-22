from django import forms
from django.forms import HiddenInput, ModelForm

from .models import Fairytale, Profile, Category, Comment


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=50, widget=forms.PasswordInput
    )  # hides the input


# class AddFairytaleForm(ModelForm):
#     class Meta:
#         model = Fairytale
#         fields = ["title", "author", "image", "body", "slug", "posted_by"]
#         widgets = {
#             "posted_by": HiddenInput()
#         }
choices = Category.objects.all().values_list('name', 'name')  # alternative for hard coding
choice_list = []

for item in choices:
    choice_list.append(item)

class AddFairytaleForm(ModelForm):
    class Meta:
        model = Fairytale
        exclude = ['posted_by', 'vector_column']
        widgets = {
            'category': forms.Select(choices = choice_list, attrs={'class':'form-controle'})
        }

class SearchForm(forms.Form):
    query = forms.CharField(label="Search term", max_length=50)

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'prefered_settings', 'image']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'


