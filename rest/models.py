from django.db import models

# Create your models here.
class user(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=200)
    msg=models.CharField(max_length=500)

    def __str__(self):
        return self.name