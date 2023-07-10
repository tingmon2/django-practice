from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.


# show user in admin panel
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
    list_filter = UserAdmin.list_filter + ("superhost",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "my_fields",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "email_verified",
                )
            },
        ),
    )
