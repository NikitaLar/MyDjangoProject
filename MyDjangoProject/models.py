from django.db import models


# Create your models here.


class authentication(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100, default=True)
    is_active = models.IntegerField()
    firstname = models.CharField(max_length=100, default=True)
    lastname = models.CharField(max_length=100, default=True)
    address = models.CharField(max_length=100, default=True)
    contactno = models.CharField(max_length=100, default=True)
    gender = models.CharField(max_length=100, default=True)

    def __str__(self):
        return self.username