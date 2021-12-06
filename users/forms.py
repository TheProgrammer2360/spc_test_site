from django import forms
from django.db.models import fields
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, CheckboxInput, Textarea
from .models import AddProperty, Bookings
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UploadPicture(forms.Form):
    profile_picture = forms.ImageField()


class UploadID(forms.Form):
    id_document = forms.FileField()


class UploadBursaryLetter(forms.Form):
    bursary_letter = forms.FileField()


class UploadProofOfRegistration(forms.Form):
    proof_of_registration = forms.FileField()

STUDENT_GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other")
)
# form for student phone number and gender
class StudentAdditionalForm(forms.Form):
    user_name = forms.CharField(min_length=3, max_length=25, widget=forms.TextInput(attrs={
        "class": "UsernameInput",
        "placeholder": "Username"
    }))
    name = forms.CharField(min_length=3, max_length=25, widget=forms.TextInput(attrs={
        "class": "UsernameInput",
        "placeholder": "Name",
    }))
    last_name = forms.CharField(min_length=3, max_length=25, widget=forms.TextInput(attrs={
        "class": "UsernameInput",
        "placeholder": "Last Name",
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "UsernameInput",
        "placeholder":"Email",
    }))
    gender = forms.ChoiceField(choices=STUDENT_GENDER, widget=forms.Select(attrs={
        "class":"UsernameInput genderSelector"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "userPassword",
        "id": "passwordInput",
        "placeholder": "Password",
    }))
    phone_number =PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial="ZA")
    )

# form for applications
class ApplicationForm(ModelForm):
    class Meta:
        model = Bookings
        fields = ["funding", "room_type"]
        exclude = ["user", "property"]
# form for adding the property


class AddPropertyForm(ModelForm):
    class Meta:
        model = AddProperty
        fields = ["accreditation_letter","lease","security","hot_water","price","discription","property_name", "email", "phone_number", "property_type", "university_catered", "address",
                  "laundromat", "unlimited_wifi", "transport", "free_electricity",
                  "single_male", "single_female", "sharing_male", "sharing_female", "main_picture", "room_picture", "kitchen_picture", "study_room_picture", "province"]
        widgets = {
            "property_name": TextInput(attrs={
                "placeholder": "Property Name...",
            }),
            "province": TextInput(attrs={
                "placeholder": "province",
            }),
            "email": EmailInput(attrs={
                "placeholder": "Email...",
            }),
            "single_female": NumberInput(attrs={
                "placeholder": "Single rooms",
            }),
            "phone_number" : PhoneNumberPrefixWidget(initial="ZA"),   
            "single_male": NumberInput(attrs={
                "placeholder": "Single rooms"
            }),
            "sharing_male": NumberInput(attrs={
                "placeholder": "Sharing rooms",
            }),
            "sharing_female": NumberInput(attrs={
                "placeholder": "Sharing rooms",
            }),
            "laundromat": CheckboxInput(attrs={
                "id": "laundromat",
            }),
            "address": Textarea(attrs={
                "rows": "5",
                "cols": "40",
            }),
            "discription": Textarea(attrs={
                "rows": "5",
                "cols": "40",
            }),
        }
        exclude = ("user",)

# class AddPropertyForm(forms.Form):
#     property_name = forms.CharField(widget=TextInput(attrs={
#         "placeholder": "Property Name...",
#         "class": "UsernameInput",
#     }), required=True)
#     property_email = forms.CharField(widget=forms.EmailInput(attrs={
#         "placeholder": "email",
#         "class": "UsernameInput",
#     }))
#     phone_number =PhoneNumberField(
#         widget=PhoneNumberPrefixWidget(initial="ZA")
#     )
#     property_type = forms.CharField(widget=forms.Select(choices=PROPERTY_CHOICES))
#     university_catered = forms.CharField(widget=forms.Select(choices=UNIVERSITY_CHOICES))
#      #  all the universities catered for
#     adress= forms.TextInput(attrs={
#         "rows": "5",
#         "cols": "40",
#     })
#     facility_wifi = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "wifi"
#     }))
#     laundromat = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "laundromat",
#     }), required=True)
#     transport = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "transport",
#     }))
#     free_electricity = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "free-electricity",
#     }))
#     unlimited_wifi = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "unlimited_wifi",
#     }))
#     single_male = forms.IntegerField(widget=forms.NumberInput(attrs={
#         "placeholder": "Single rooms",
#     })),
#     single_female = forms.IntegerField(widget=forms.NumberInput(attrs={
#         "placeholder": "Single rooms",
#     })),
#     sharing_male = forms.IntegerField(widget=forms.NumberInput()),
#     sharing_female = forms.IntegerField(widget=forms.NumberInput(attrs={
#         "placeholder": "Sharing rooms",
#     })),
#     main_picture = forms.ImageField()
#     room_picture = forms.ImageField()
#     kitchen_picture = forms.ImageField()
#     study_ro0m_picture = forms.ImageField()

# Form to register The property owner


class PropertyGeneralInfo(forms.Form):
    property_username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "placeholder": "Company Username",
        "class": "UsernameInput",
    }))

    property_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Company Name",
        "class": "UsernameInput",
    }))
    property_email = forms.CharField(widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "UsernameInput",
    }))
    property_phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial="ZA")
    )
    password = forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={
        'placeholder': "Password",
        "class": "userPassword",
    }))
    
class EditPropertyAccount(forms.Form):
    property_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Company Name",
        "class": "UsernameInput",
    }))
    property_phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial="ZA")
    )
    property_email = forms.CharField(widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "UsernameInput",
    }))