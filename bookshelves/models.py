from django.db import models


class Bookshelf(models.Model):
    name = models.CharField(blank=False, max_length=100, default="")
