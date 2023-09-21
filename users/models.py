from django.db import models

# Create your models here.

class User(models.Model):
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  email = models.CharField(max_length=20)
  username = models.CharField(max_length=20)
  password = models.CharField(max_length=50)
  
def __str__(self):
  return f'{self.first_name} {self.last_name}'