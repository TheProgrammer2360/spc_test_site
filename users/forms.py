from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, CheckboxInput
from .models import AddProperty


class UploadPicture(forms.Form):
    profile_picture = forms.ImageField()


class UploadID(forms.Form):
    id_document = forms.FileField()


class UploadBursaryLetter(forms.Form):
    bursary_letter = forms.FileField()


class UploadProofOfRegistration(forms.Form):
    proof_of_registration = forms.FileField()

# form for adding the property


class AddPropertyForm(ModelForm):
    class Meta:
        model = AddProperty
        fields = ["property_name", "email", "phone_number", "property_type", "university_catered", "address",
                  "laundromat", "unlimited_wifi", "transport", "free_electricity",
                  "single_male", "single_female", "sharing_male", "sharing_female"]
        widgets = {
            "property_name": TextInput(attrs={
                "placeholder": "Property Name...",
            }),
            "email": EmailInput(attrs={
                "placeholder": "Email...",
            }),
            "phone_number": NumberInput(attrs={
                "placeholder": "Cell phone number...",
            }),
            "single_female": NumberInput(attrs={
                "placeholder": "Single rooms",
            }),
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
            })
        }

# class AddProperty(forms.Form):
#     property_email = forms.CharField(widget=forms.EmailInput(attrs={
#         "placeholder": "email",
#     }))
#     property_phone_number = forms.CharField(widget=forms.NumberInput(attrs={
#         "placeholder": "Phone number",
#     }))
#
#     property_type = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple, choices=PROPERTY_CHOICES)
#     university_catered = forms.CharField(widget=forms.Select(choices=UNIVERSITY_CHOICES))
#     #  all the universities catered for
#     facility_wifi = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "wifi"
#     }))
#     facility_laundromat = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "laundromat",
#     }))
#     facility_transport = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "transport",
#     }))
#     facility_free_electricity = forms.BooleanField(widget=forms.CheckboxInput(attrs={
#         "id": "free-electricity",
#     }))

# Form to register The property owner


class PropertyGeneralInfo(forms.Form):
    property_username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "placeholder": "Unique Username",
    }))

    property_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Property name...",
    }))
    property_email = forms.CharField(widget=forms.EmailInput(attrs={
        "placeholder": "Email",
    }))
    property_phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        "placeholder": "Phone number...",
    }))
    password = forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'placeholder': "Password..."}))
