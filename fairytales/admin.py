from django.contrib import admin
from .models import Fairytale, Profile, Category, Comment

# Register your models here.


admin.site.register(Fairytale)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comment)
