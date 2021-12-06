from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from phonenumber_field.modelfields import PhoneNumberField

STUDENT_GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other")
)
class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=STUDENT_GENDER)
    phone_number = PhoneNumberField()


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
    ("UJ1", "UJ(APK)"),
    ("UJ2", "UJ(APB)"),
    ("UJ3", "UJ(DFC)"),
    ("UJ4", "UJ(  SWC)"),
    ("NWU1", "NWU-Mafikeng campus"),
    ("NWU2", "NWU-Vaal campus"),
    ("NWU3", "NWU-Potchefstroom campus"),
    ("TUT", "TUT"),
    ("WITS", "WITS"),
    ("UP", "WITS"),
    ("CUT", "CUT"),
    ("VUT", "VUT"),
    ("UWC", "UWC"),
    ("UFS", "UFS"),
)


class AddProperty(models.Model):
    id = models.AutoField(primary_key=True)
    main_picture = models.ImageField(upload_to="images/", null=False)
    room_picture = models.ImageField(upload_to="images/", null=True)
    kitchen_picture = models.ImageField(upload_to="images/", null=True)
    study_room_picture = models.ImageField(upload_to="images/", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=25)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    property_type = models.CharField(max_length=9, choices=PROPERTY_CHOICES)
    university_catered = models.CharField(max_length=4, choices=UNIVERSITY_CHOICES)
    address = models.TextField()
    province = models.CharField(max_length=20)
    laundromat = models.BooleanField()
    security = models.BooleanField()
    hot_water = models.BooleanField()
    unlimited_wifi = models.BooleanField()
    transport = models.BooleanField()
    free_electricity = models.BooleanField()
    single_male = models.IntegerField()
    single_female = models.IntegerField()
    sharing_female = models.IntegerField()
    sharing_male = models.IntegerField()
    discription = models.TextField()
    price = models.FloatField()
    accreditation_letter = models.FileField(upload_to="documents/", null=True)
    lease = models.FileField(upload_to="documents/", null=True)


FUNDING = (
        ("NSFAS", "NSFAS"),
        ("BURSARY", "Bursary"),
        ("SELF FUNDED", "Self Funded ")
)

ROOM_TYPE = (
    ("SHARING", "Sharing"),
    ("SINGLE", "Single")
)
STATUS = (
    ("ACCEPTED", "Accepted"),
    ("DECLINED", "Declined"),
    ("PENDING", "Pending"),
)


class Bookings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(AddProperty, on_delete=models.CASCADE)
    funding = models.CharField(max_length=11, choices=FUNDING)
    room_type = models.CharField(max_length=7, choices=ROOM_TYPE)
    status = models.CharField(max_length=8, choices=STATUS)