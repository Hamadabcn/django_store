# blog/models.py

from django.db import models
from .author import Author  # Correct import based on directory structure
from django.utils import timezone


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
