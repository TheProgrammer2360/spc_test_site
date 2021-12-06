from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("account_type", views.profile_info, name="account_type"),
    path("login", views.login_view, name="login"),
    path("create", views.create_account, name="create"),
    path("logout", views.logout_view, name="logout"),
    path("image_upload", views.image_upload, name="image_upload"),
    path("create_property_account", views.create_property_account, name="create_property_account"),
    path("student_info", views.index, name="student_info"),
    path("student_account", views.student_details, name="student_details"),
    path("property_account", views.property_account, name="property_account"),
    path("account_creation_type", views.account_creation_type, name="account_creation_type"),
    path("register_property_owner", views.register_property_owner, name="register_property_owner"),
    path("id_upload", views.id_upload, name="id_upload"),
    path("view_id_document", views.view_id_document, name="view_id_document"),
    path("property_owner_profile", views.property_owner_profile, name="property_owner_profile"),
    path("add_property", views.add_property, name="add_property"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("edit_student_profile", views.edit_student_profile, name="edit_student_profile"),
    path("get_all_property", views.properties, name="get_all_property"),
    path("property/<int:id>", views.property_profile, name="property" ),
    path("edit_property_account", views.edit_property_account, name="edit_property_account"),
    path("view_property_owner/<int:number>", views.owner_view, name="owner_view"),
    path("delete_property/<int:number>", views.delete_property, name="owner_delete"),
    path("edit_property/<int:number>", views.edit_property, name="edit_property"),
    path("properties/<str:property_type>", views.view_properties_filter, name="view_properties_filter"),
    path("add_property", views.add_property, name="add_property"),
    path("property_view/<int:id>", views.view_property_as_student, name="view_property_as_student"),
    path("book_room/<int:id>", views.book_room, name="book_room"),
]
