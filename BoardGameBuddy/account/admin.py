from django.contrib import admin

from django.contrib.auth import admin as auth_admin, get_user_model
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from BoardGameBuddy.account.forms import SignUpForm, AccountEditForm
from BoardGameBuddy.account.models import BuddyProfile

UserModel = get_user_model()


@admin.register(UserModel)
class BuddyAdmin(auth_admin.UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),

        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = AccountEditForm
    add_form = SignUpForm
    change_password_form = auth_forms.AdminPasswordChangeForm
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(BuddyProfile)
class BuddyProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'age', 'location', 'first_name', 'last_name', 'is_public', 'account_id')
    list_filter = ('nickname', 'age', 'location', 'first_name', 'last_name', 'is_public', 'account_id')
    search_fields = ('nickname', 'age', 'location', 'first_name', 'last_name', 'is_public', 'account_id')

    ordering = ("account_id",)
