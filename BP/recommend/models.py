from django.db import models

# Create your models here.

class Genre(models.Model) :
    title = models.TextField()
    isbn13 = models.TextField()
    categories = models.TextField(null=True)
    cover = models.TextField()
    def __str__(self):
        return self.name
