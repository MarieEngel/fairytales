from django.db import models

# Create your models here.


class Fairytale(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    body = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
