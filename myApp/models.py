from django.db import models
from django.conf import settings
from accounts.models import CustomUser , G
# import accounts.models 
from django.core.validators import FileExtensionValidator
# Create your models here.


def get_upload_path(instance, filename):
    return 'documents/{0}/{1}'.format(instance.owner.username, instance.name)


class File(models.Model):
    name = models.CharField(max_length=50 , unique=True)
    file = models.FileField(upload_to=get_upload_path )
    owner  = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    block  = models.ForeignKey(CustomUser, null=True,on_delete=models.SET_NULL  ,blank=True , related_name='block')
    

    content = models.TextField(default="none")
    createdDate  = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(G) 

    def __str__(self):
        return self.name 
