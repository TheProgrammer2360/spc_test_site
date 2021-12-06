from django.core.mail.message import ADDRESS_HEADERS
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, logout, login
from .models import AddProperty, Student, Profiles, Identity, Bookings
from .forms import UploadPicture, UploadID, UploadBursaryLetter, UploadProofOfRegistration, PropertyGeneralInfo
from .forms import AddPropertyForm, StudentAdditionalForm, EditPropertyAccount, ApplicationForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm


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


def create_user_account(user_name, name, email, password, last_name, phone_number, gender):
    """Creates a user  using name, email and password"""
    user = User.objects.create_user(user_name, email, password)
    user.first_name = name
    user.last_name = last_name
    user.save()
    student_permissions = ["view_property", "apply_for_resident", "edit_student_information",
                           "view_student_information", "upload_id", "book_room"]
    add_permissions(student_permissions)
    for permission_name in student_permissions:
        permission = Permission.objects.get(codename=permission_name)
        user.user_permissions.add(permission)
    user_info = Student(user=user, phone_number=phone_number, gender=gender)
    user_info.save()


def edit_property_owner_account(user, property_name, email, phone_number):
    """edits the details of the property owner"""
    user.first_name = property_name
    user.email = email
    user.save()
    # the phone number part
    user.student.phone_number = phone_number
    user_infor = user.student
    user_infor.save()
    

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
    user_info = Student(user=user, phone_number=phone_number)
    user_info.save()

# route to determine which type of user to create_user


def account_creation_type(request):
    return render(request, "users/account_creation_type.html")


@login_required(login_url="/users/login")
@permission_required("auth.create_property")
def add_property(request):
    if request.method == "POST":
        form_data = AddPropertyForm(request.POST, request.FILES)
        if form_data.is_valid():
            property = form_data.save(commit=False)
            property.user = request.user
            property.save()
            return HttpResponseRedirect(reverse("users:property_owner_profile"))
        else:
            form = AddPropertyForm()
            return render(request, "users/add_property.html", {
                "form": form,
            })
    form = AddPropertyForm()
    return render(request, "users/add_property.html", {
        "form": form,
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
    # checking the gender
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
    """deals with what happens when the user visits the login page"""
    if request.method == "POST":
        username = request.POST["user_name"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            # log the user in , if the user credentials are valid
            login(request, user)
            # check if user is a student or property owner
            is_student = user.has_perm("auth.view_student_information")
            is_property_owner = user.has_perm("auth.view_property_account")
            if is_student:
                # when the user is from student account
                return HttpResponseRedirect(reverse("users:student_info"))
            elif is_property_owner:
                # when user is a property owner
                return HttpResponseRedirect(reverse("users:property_owner_profile"))
            else:
                return HttpResponseRedirect(reverse("users:login"))
        else:
            return render(request, "users/login.html", {
                "message": "Your username and password do not match"
            })
    return render(request, "users/login.html")


def create_account(request):
    """For students"""
    # if user has registered successfully
    if request.method == "POST":
        # getting student information from the form
        student_form = StudentAdditionalForm(request.POST)
        # getting the stud
        if student_form.is_valid():
            # getting user info
            user_name = student_form.cleaned_data['user_name']
            first_name = student_form.cleaned_data['name'].title()
            email = student_form.cleaned_data['email']
            password = student_form.cleaned_data['password']
            last_name = student_form.cleaned_data['last_name'].title()
            phone_number = student_form.cleaned_data['phone_number']
            gender = student_form.cleaned_data['gender']
            try:
                print("creating user...")
                create_user_account(user_name=user_name, name=first_name,email=email,password=password, last_name=last_name,phone_number=phone_number, gender=gender)
                print("User created")
            except IntegrityError:
                # send message if the user is taken
                print("user exits")
                return render(request, "users/account_creation.html", {
                    "user_exist": "The username that you have chosen is not available try another one"
                })
        else:
            print("Form is not valid")
        # saving the phone number and creating additional user information
            return HttpResponseRedirect(reverse("users:login"))
    form = StudentAdditionalForm()
    return render(request, "users/account_creation.html", {
        "form": form
    })


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
    # propeties under this user
    properties = AddProperty.objects.filter(user=user_logged)
    return render(request, "users/property_owner_profile.html", {
        "user": user_logged,
        "properties": properties,
    })

def password_reset_request(request):
    if request.method == "POST":
	    password_reset_form = PasswordResetForm(request.POST)
	    if password_reset_form.is_valid():
		    data = password_reset_form.cleaned_data['email']
		    associated_users = User.objects.filter(email=data)
		    if associated_users.exists():
			    for user in associated_users:
				    subject = "Password Reset Requested"
				    email_template_name = "users/password/password_reset_email.txt"
				    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'SPC Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
				    email = render_to_string(email_template_name, c)
				    try:
				    	send_mail(subject, email, 'proking.lover@gmail.com' , [user.email], fail_silently=False)
				    except BadHeaderError:
				        return HttpResponse('Invalid header found.')
				    return redirect ("/password_reset/done")
    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required(login_url="/users/login")
@permission_required("auth.edit_student_information")
def edit_student_profile(request):
   return render(request, "users/edit.html")


def properties(request):
    """it gets all tthe properties from the database"""
    data = AddProperty.objects.all
    property = {
        "properties": data
    }
    return render(request, "users/properties.html", property)

def property_profile(request, id):
    """gets the data sent by property"""
    data = AddProperty.objects.get(id=id)
    property_details = {
        "details": data
    }
    return render(request, "users/property.html", property_details)


@login_required
@permission_required("auth.edit_property_account")
def edit_property_account(request):
    if request.method == "POST":
        form_data = EditPropertyAccount(request.POST)
        if form_data.is_valid():
            property_name = form_data.cleaned_data["property_name"]
            property_email = form_data.cleaned_data["property_email"]
            property_phone = form_data.cleaned_data["property_phone"]
            edit_property_owner_account(user=request.user, property_name=property_name,email=property_email, phone_number=property_phone)
            return HttpResponseRedirect(reverse("users:property_owner_profile"))
    
    form = EditPropertyAccount()
    return render(request, "users/edit_property_account.html", {
        "form": form
    })

@login_required
@permission_required("auth.edit_property")
def owner_view(request, number):
    data = AddProperty.objects.get(id=number)
    # get the list of bookings
    bookings = Bookings.objects.filter(property=data)
    print(bookings)
    return render(request, "users/owner_view_property.html", {
        "property": data,
        "bookings":bookings,
    })
@login_required
@permission_required("auth.edit_property")
def delete_property(request, number):
    data = AddProperty.objects.get(id=number)
    if data.user == request.user:
        data.delete()
        return HttpResponseRedirect(reverse("users:property_owner_profile"))
    else:
        return HttpResponse("property doest not exist")

@login_required
@permission_required("auth.edit_property")
def edit_property(request, number):
    if request.method == "POST":
        form = AddPropertyForm(request.POST, request.FILES,instance=AddProperty.objects.get(id=number))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:property_owner_profile"))
        else:
            user = request.user
            # get the property using the the id
            property_to_be_edited = AddProperty.objects.get(id=number)
            instance = AddPropertyForm(instance=property_to_be_edited)
            
            return render(request, "users/edit_property.html", {
                "form": instance,
                "error_message": "invalid message done",
                "property_number": number
            })

    user = request.user
    # get the property using the the id
    property_to_be_edited = AddProperty.objects.get(id=number)
    instance = AddPropertyForm(instance=property_to_be_edited)

    return render(request, "users/edit_property.html", {
        "form": instance,
        "property_number": number,
    })

def view_properties_filter(request, property_type):
    get_properties = AddProperty.objects.all().filter(property_type=property_type.upper())
    print(get_properties)
    return render(request, "users/view_properties.html", {
        "properties": get_properties
    })

@login_required(login_url="/users/login")
#@permission_required("auth.apply_for_resident"):
def view_property_as_student(request, id):
    # get property requested by student
    property = AddProperty.objects.get(id=id)
    print(property.main_picture.url)
    return render(request, "users/view_property_student.html", {
        "property": property
    })

@login_required
#@permission_required("auth.book_room")
def book_room(request, id):
    # get the property you are applying for
    property = AddProperty.objects.get(id=id)
    if request.method == "POST":
        # get the post data
        data = ApplicationForm(request.POST)
        if data.is_valid():
            booking = data.save(commit=False)
            booking.user = request.user
            booking.property = property
            booking.save()
    student_applying = request.user
    # form for bookings
    bookings = ApplicationForm()
    return render(request, "users/book_room.html", {
        "property": property,
        "student": student_applying,
        "application": bookings
    })

