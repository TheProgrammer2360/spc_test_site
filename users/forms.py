from django import forms
from .models import Student

class UploadPicture(forms.Form):
    profile_picture = forms.ImageField()

class UploadID(forms.Form):
    id_document = forms.FileField()

class UploadBursaryLetter(forms.Form):
    bursary_letter = forms.FileField()

class UploadProofOfRegistration(forms.Form):
    proof_of_registration =forms.FileField()

# Form to register The property owner
class PropertyGeneralInfo(forms.Form):
    property_username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={
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
