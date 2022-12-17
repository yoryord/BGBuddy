from django.apps import apps
from django.contrib import auth
from django.contrib.auth import base_user
from django.contrib.auth.hashers import make_password
from django.contrib.auth import models as auth_models
from django.core import validators

from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from BoardGameBuddy.account.cust_validators import validate_file_size, validate_nickname_chars, validate_names_chars


class BuddyManager(base_user.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(
            self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class BuddyAccount(base_user.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(_("email address"),
                              null=False,
                              blank=False,
                              unique=True
                              )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = BuddyManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user email")
        verbose_name_plural = _("user emails")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class BuddyProfile(models.Model):

    MAX_LEN_NICKNAME = 15
    MIN_LEN_NICKNAME = 2
    MAX_LEN_NAMES = 30
    MAX_LEN_PERS_INTERESTS = 300
    MAX_LEN_LOCATION = 50

    nickname = models.CharField(
        max_length=MAX_LEN_NICKNAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_NICKNAME, message='Nickname must consist of minimum 2 chars'),
            validate_nickname_chars,
        ),
        null=True,
        blank=False,
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=False,
    )

    location = models.CharField(
        max_length=MAX_LEN_LOCATION,
        null=True,
        blank=False,
    )

    first_name = models.CharField(
        max_length=MAX_LEN_NAMES,
        validators=(validate_names_chars,),
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_LEN_NAMES,
        validators=(validate_names_chars,),
        null=True,
        blank=True,
    )

    personal_interests = models.TextField(
        max_length=MAX_LEN_PERS_INTERESTS,
        help_text=_('(max 300 characters)'),
        null=True,
        blank=True,
    )

    is_public = models.BooleanField(
        default=True,
        help_text=_('Share your personal info'),

    )


    profile_picture = models.ImageField(
        upload_to='profile_photos',
        validators=(validate_file_size,),
        null=True,
        blank=True,
    )

    account_id = models.OneToOneField(to=BuddyAccount,
                                      primary_key=True,
                                      on_delete=models.CASCADE,
                                      )

    # Since BuddyProfile instance is created right after BuddyAccount,
    # the nickname could be "None", thus a default string is put.
    def __str__(self):
        return self.nickname or "no nickname yet"

    # Below refers to BuddyGuild reversed relation 'members_set'
    # and checks whether current BuddyProfile is member in any BuddyGuild
    def has_guild(self):
        members = self.members_set.all()

        if members:
            return True
        return False

