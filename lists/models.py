from __future__ import unicode_literals

from django.db import models


class Item(models.Model):
    text = models.TextField(default="")
    list = models.TextField(default="")


class List(models.Model):
    pass

