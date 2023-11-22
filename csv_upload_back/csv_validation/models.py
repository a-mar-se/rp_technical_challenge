from django.db import models
from django import forms
from django.core import validators


class Entity(models.Model):
    entity_id = models.CharField(max_length=8)
    data_type = models.CharField(max_length=16)
    data_value = models.CharField(max_length=256)
