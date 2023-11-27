from django.db import models
from django import forms
from django.core import validators

from .validators import data_type_validator


class Entity(models.Model):
    entity_id = models.CharField(max_length=8)
    data_type = models.CharField(max_length=16)
    data_value = models.CharField(max_length=256, validators=[data_type_validator])

    REQUIRED_FIELDS = ['entity_id','data_type','data_value']