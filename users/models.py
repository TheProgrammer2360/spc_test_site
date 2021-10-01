from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)


class Profiles(models.Model):
    profile_picture = models.ImageField(upload_to="images/", null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

# model the id document
class Identity(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    document = models.FileField(upload_to="documents/", null=True)
