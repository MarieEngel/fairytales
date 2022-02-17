from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
# Create your models here.


class Fairytale(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    body = models.TextField()
    slug = models.SlugField(unique=True)
    vector_column = SearchVectorField(null=True)  # don't use 'models.' before search

    class Meta:
        indexes = (GinIndex(fields=["vector_column"]),)

    def __str__(self):
        return f"{self.title} - {self.author}"
