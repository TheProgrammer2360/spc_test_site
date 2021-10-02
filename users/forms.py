from django import forms


class UploadPicture(forms.Form):
    profile_picture = forms.ImageField()


class UploadID(forms.Form):
    id_document = forms.FileField()


class UploadBursaryLetter(forms.Form):
    bursary_letter = forms.FileField()


class UploadProofOfRegistration(forms.Form):
    proof_of_registration = forms.FileField()

# form for adding the property


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


class AddProperty(forms.Form):
    property_email = forms.CharField(widget=forms.EmailInput(attrs={
        "placeholder": "email",
    }))
    property_phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        "placeholder": "Phone number",
    }))

    property_type = forms.CharField(widget=forms.Select(choices=PROPERTY_CHOICES))
    university_catered = forms.CharField(widget=forms.Select(choices=UNIVERSITY_CHOICES))
    #  all the universities catered for
    facility_wifi = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "id": "wifi"
    }))
    facility_laundromat = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "id": "laundromat",
    }))
    facility_transport = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "id": "transport",
    }))
    facility_free_electricity = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "id": "free-electricity",
    }))

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
