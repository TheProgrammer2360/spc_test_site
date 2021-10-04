from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)


class Profiles(models.Model):
    profile_picture = models.ImageField(upload_to="images/", null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)


class Identity(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    document = models.FileField(upload_to="documents/", null=True)


PROPERTY_CHOICES = (
        ("COMMUNE", "Commune"),
        ("APARTMENT", "Apartment"),
        ("FLAT", "flat")
)
UNIVERSITY_CHOICES = (
    ("UJ", "UJ"),
    ("NWU", "NWU"),
    ("TUT", "TUT"),
    ("WITS", "WITS"),
    ("UP", "WITS"),
    ("CUT", "CUT"),
    ("VUT", "VUT"),
    ("UWC", "UWC"),
    ("UFS", "UFS"),
)


class AddProperty(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    property_type = models.CharField(max_length=9, choices=PROPERTY_CHOICES)
    university_catered = models.CharField(max_length=4, choices=UNIVERSITY_CHOICES)
    address = models.TextField()
    province = models.CharField(max_length=20)
    laundromat = models.BooleanField()
    unlimited_wifi = models.BooleanField()
    transport = models.BooleanField()
    free_electricity = models.BooleanField()
    single_male = models.IntegerField()
    single_female = models.IntegerField()
    sharing_female = models.IntegerField()
    sharing_male = models.IntegerField()

