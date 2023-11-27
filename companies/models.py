from django.db import models

class Companie(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    address = models.TextField()
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name