from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=30)
    upassword = models.CharField(max_length=10)
    uemail = models.EmailField(null=True, blank=True)
