from django.db import models


# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass
    


class G(models.Model):
    name = models.CharField(max_length=255 , unique=True)
    owner = models.ForeignKey(CustomUser , null=True , on_delete=models.SET_NULL  , related_name='owner' ) 
    users = models.ManyToManyField(CustomUser)
    def __str__(self):
        return self.name 






