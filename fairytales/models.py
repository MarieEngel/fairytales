from .make_thumbnail import make_thumbnail
from .add_flag import add_flag
from io import BytesIO
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from PIL import Image
from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent

class Fairytale(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    thumbnail = models.ImageField(null=True, blank=True, upload_to="images/")
    with_flag = models.ImageField(null=True, blank=True, upload_to="images/")
    body = models.TextField()
    slug = models.SlugField(unique=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    vector_column = SearchVectorField(null=True)  # don't use 'models.' before search
    category = models.CharField(max_length=100, default="uncategorized")

    class Meta:
        indexes = (GinIndex(fields=["vector_column"]),)

    def __str__(self):
        return f"{self.title} - {self.author}"

    def save(self, *args, **kwargs):
        self.thumbnail = make_thumbnail(self.image, size=(100, 100))
        self.with_flag = add_flag(self.image)
        super().save(*args, **kwargs)



    # def save(self, *args, **kwargs):
    #     self.image.save()
    #     flag_path = os.path.join(BASE_DIR, 'static/fairytales/flag.png')
    #     current_image_path = os.path.join(BASE_DIR.parent, self.image.url[1:])
    #     flag = Image.open(flag_path)
    #     im = Image.open(current_image_path)
    #     flag = Image.open(flag_path)
    #     im = Image.open(self.image)
    #     # output = BytesIO()
    #     name, suffix = self.image.split('.')
    #     image_copy = im.copy()
    #     position = ((image_copy.width - flag.width), (image_copy.height - flag.height))
    #     image_copy.paste(flag, position)
    #     # image_copy.save(output, format='JPEG')
	# 	# output.seek(0)
    #     image_copy.save(f'{name}_flag{suffix}')

        # self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0])

        # super(Fairytale,self).save()
        # img = Image.open(self.image.path) # Open image
        # if img.height > 200 or img.width > 200:
        #     output_size = (200, 200)
        #     img.thumbnail(output_size) # Resize image
        #     img.save(self.image.path) # Save it again and override the larger 

    




class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    prefered_settings = models.JSONField(null=True, blank=True)
    image = models.ImageField(
        default="profile_pics/default.png", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.username} Profile"


class Comment(models.Model):
    fairytale = models.ForeignKey(
        Fairytale, related_name="comments", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fairytale.title} - {self.name}"
