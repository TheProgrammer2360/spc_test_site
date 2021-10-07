from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, logout, login
from .models import Student, Profiles, Identity
from .forms import UploadPicture, UploadID, UploadBursaryLetter, UploadProofOfRegistration, PropertyGeneralInfo
from .forms import AddPropertyForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError


def add_permissions(permissions):
    for permission in permissions:
        try:
            content_type = ContentType.objects.get_for_model(User)
            Permission.objects.create(
                codename=permission,
                content_type=content_type,
            )
        except IntegrityError:
            pass


def create_user_account(user_name, name, email, password, last_name, phone_number):
    """Creates a user  using name, email and password"""
    user = User.objects.create_user(user_name, email, password)
    user.first_name = name
    user.last_name = last_name
    user.save()
    student_permissions = ["view_property", "apply_for_resident", "edit_student_information",
                           "view_student_information", "upload_id"]
    add_permissions(student_permissions)
    for permission_name in student_permissions:
        permission = Permission.objects.get(codename=permission_name)
        user.user_permissions.add(permission)
    user_info = Student(user=user, phone_number=phone_number)
    user_info.save()
    print(user.has_perm("auth.apply_for_resident"))


def create_property_owner_account(user_name, property_name, email, password, phone_number):
    """Create a property_owner user account with its own permission"""
    user = User.objects.create_user(user_name, email, password)
    # always remember first name is the property_name
    user.first_name = property_name
    # create a permission if they are not there
    property_owner_permissions = ["view_property_account", "edit_property_account", "create_property", "view_property",
                                  "edit_property", "view_student_application"]
    add_permissions(property_owner_permissions)
    # adding the permissions to this users
    for permission_name in property_owner_permissions:
        permission = Permission.objects.get(codename=permission_name)
        user.user_permissions.add(permission)
    # saving user with all the permissions of property Owner
    user.save()
    # saving property owners phone number
    Student(user=user, phone_number=phone_number)

# route to determine which type of user to create_user


def account_creation_type(request):
    return render(request, "users/account_creation_type.html")


@login_required(login_url="/users/login")
@permission_required("auth.create_property")
def add_property(request):
    form_data = AddPropertyForm()
    return render(request, "users/add_property.html", {
        "form": form_data
    })


@login_required(login_url="users/login")
@permission_required("auth.upload_id")
def id_upload(request):
    """uploads the documents of the user"""
    if request.method == 'POST':
        form = UploadID(request.POST, request.FILES)
        if form.is_valid():
            # saves the id document of student_
            save_id_document = Identity(user=request.user, document=form.cleaned_data["id_document"])
            save_id_document.save()
            # returning user to their profile
            return render(request, "users/index.html", {
                "id_upload_message": "You have successfully uploaded your ID",
                "UploadPicture": UploadPicture(),
                "bursary_letter": UploadBursaryLetter(),
                "proof_of_registration": UploadProofOfRegistration,
                "id": UploadID,
            })
    else:
        return HttpResponseRedirect("users:student_account")


@login_required(login_url="/users/login")
def view_id_document(request):
    return render(request, "users/view_id_document.html", {
        "url_p": request.user.identity.document.url,
    })


@login_required(login_url="/users/login")
def image_upload(request):
    """saves the file"""
    if request.method == 'POST':
        # getting the user inform
        form = UploadPicture(request.POST, request.FILES)
        if form.is_valid():
            # don't forget to delete the current user image b4 updating
            create_user_profile = Profiles(user=request.user, profile_picture=form.cleaned_data["profile_picture"])
            create_user_profile.save()
            print(request.user.profiles.profile_picture.path)
            # checking to see if the image is indeed save
    return HttpResponseRedirect(reverse("users:student_info"))
# Create your views here.


def profile_info(request):
    # route for for when the user is logged in as Student
    user_student_account = request.user.has_perm("auth.view_student_information")
    property_owner_account = request.user.has_perm("auth.view_property_account")
    if user_student_account:
        return HttpResponseRedirect(reverse("users:student_info"))
        # don't forget the on when the property owner is logged in
    elif property_owner_account:
        return HttpResponseRedirect("users:property_owner_profile")
    else:
        # when no one is logged in
        return HttpResponseRedirect(reverse("users:login"))


@permission_required("auth.view_student_information")
def index(request):
    return render(request, "users/index.html", {
        "UploadPicture": UploadPicture(),
        "bursary_letter": UploadBursaryLetter(),
        "proof_of_registration": UploadProofOfRegistration,
        "id": UploadID,
    })


@login_required(login_url="/users/login")
def student_details(request):
    user_student_permission = request.user.has_perm("auth.view_student_information")
    if user_student_permission:
        return HttpResponseRedirect(reverse("users:student_info"))
    else:
        return render(request, "main_website/home.html", {
                "Not_a_student": "You have logged in with a Property Owner account"
                                 ", please sign out and log in with ur user account",
            })


def login_view(request):
    if request.method == "POST":
        username = request.POST["user_name"]
        password = request.POST["password"]
        # check if user details are fine
        print(username)
        user = authenticate(username=username, password=password)
        if user is not None:
            # login in user
            login(request, user)
            # check if user is a student or property owner
            is_student = user.has_perm("auth.view_student_information")
            if is_student:
                return HttpResponseRedirect(reverse("users:student_info"))
            else:
                return HttpResponseRedirect(reverse("users:property_owner_profile"))
        else:
            return render(request, "users/login.html", {
                "message": "Your username and password do not match"
            })
    return render(request, "users/login.html")


def create_account(request):
    # if user has registered successfully
    if request.method == "POST":
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        user_name = request.POST["user_name"]
        phone_number = request.POST["phone_number"]
        try:
            create_user_account(user_name, first_name, email, password, last_name, phone_number)
        except IntegrityError:
            # send message if the user is taken
            return render(request, "users/account_creation.html", {
                "user_exist": "The username that you have chosen is not available try another one"
            })
        # saving the phone number and creating additional user information
        return HttpResponseRedirect(reverse("users:login"))

    return render(request, "users/account_creation.html")


def property_account(request):
    """"Property for when user presses property on navbar"""
    # checking if the user in a student/ don't forget to change the permission
    is_user_student = request.user.has_perm("auth.view_student_accounts")
    print(is_user_student)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    elif is_user_student:
        student_logged_in = "You are currently logged in as a student please logout" \
                            " and login with you property owner account"
        return render(request, "main_website/home.html", {
            "student_logged_in": student_logged_in,
        })
    else:
        return HttpResponseRedirect(reverse("users:property_owner_profile"))


def create_property_account(request):
    """"takes the user to create  property form"""
    form = PropertyGeneralInfo()
    return render(request, "users/register_property_owner.html", {
        "form": form,
    })


@login_required(login_url='/users/login')
def logout_view(request):
    """Logs the user out"""
    logout(request)
    logout_message = "You have successfully logged out"
    return render(request, "users/login.html", {
        "logout_message": logout_message
    })


def register_property_owner(request):
    """"route that will register the property owner"""
    # getting property owner info
    user_info = PropertyGeneralInfo(request.POST)
    if user_info.is_valid():
        user_name = user_info.cleaned_data["property_username"]
        property_name = user_info.cleaned_data["property_name"]
        property_email = user_info.cleaned_data["property_email"]
        phone_number = user_info.cleaned_data["property_phone"]
        password = user_info.cleaned_data["password"]
        # create account
        create_property_owner_account(user_name, property_name, property_email, password, phone_number)
        # log the user in
        user = authenticate(request, password=password, username=user_name)
        login(request, user)
        return HttpResponseRedirect(reverse("users:property_owner_profile"))
        # redirect the user to their profile


@login_required(login_url="/users/login")
@permission_required("auth.view_property_account")
def property_owner_profile(request):
    user_logged = request.user
    return render(request, "users/property_owner_profile.html", {
        "user": user_logged,
    })
