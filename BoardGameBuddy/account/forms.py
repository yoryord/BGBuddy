from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from django.utils.translation import gettext_lazy as _

from BoardGameBuddy.account.models import BuddyProfile

UserModel = get_user_model()


class SignUpForm(auth_forms.UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autocomplete": "email address"}),
        # help_text=_("Enter your email"),
    )

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)
        # field_classes = {"email": UsernameField}


class AccountEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = "__all__"
        # field_classes = {"username": UsernameField}


class BuddyProfileEditForm(forms.ModelForm):
    class Meta:
        model = BuddyProfile
        exclude = ('account_id',)

        labels = {
            'nickname': "",
            'age': "",
            'location': "",
            'first_name': "",
            'last_name': "",
            'personal_interests': "",
            'profile_picture': "",
            'is_public': "Public",
        }

        widgets = {
            'nickname': forms.TextInput(
                attrs={
                    'placeholder': "Enter nickname",
                }
            ),
            'age': forms.TextInput(
                attrs={
                    'placeholder': "Enter age",
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'placeholder': "Enter location",
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': "Enter first name",
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': "Enter last name",
                }
            ),
            'personal_interests': forms.Textarea(
                attrs={
                    'placeholder': "Add information regarding your personal interests, etc.",
                }
            ),
            'profile_picture': forms.FileInput(),
        }


class BuddyPasswordChangeForm(auth_forms.PasswordChangeForm):
    pass

# TODO remove later
# class PassChangeForm(auth_forms.AdminPasswordChangeForm):
#     pass

# PasswordChangeForm
