from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_block = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Usuário válido até {self.date_block}'
