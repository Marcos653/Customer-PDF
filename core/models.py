from distutils.command.upload import upload
from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    cpf = models.CharField(max_length=14, null=False, blank=False)
    photo = models.ImageField(upload_to='image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name   
