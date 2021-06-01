from django.db import models
from django.contrib.auth.models import AbstractUser

def get_default_dict():
    return {'slots': []}

class User(AbstractUser):
    is_candidate = models.BooleanField(default=True)
    slots = models.JSONField(default=get_default_dict)