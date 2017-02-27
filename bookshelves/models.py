from django.db import models


class Bookshelf(models.Model):
    name = models.CharField(blank=False, max_length=100, default="")


class Book(models.Model):
    name = models.CharField(blank=False, max_length=60, default="")
    bookshelf = models.ForeignKey(
        Bookshelf,
        on_delete=models.CASCADE,
        default=None,
    )
