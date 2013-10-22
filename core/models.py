from django.contrib.auth.models import User
from django.db import models

from .utils import create_slug


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta():
        abstract = True


