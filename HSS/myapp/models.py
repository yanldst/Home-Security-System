from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mode(models.Model):
    name = models.CharField(max_length=50)
