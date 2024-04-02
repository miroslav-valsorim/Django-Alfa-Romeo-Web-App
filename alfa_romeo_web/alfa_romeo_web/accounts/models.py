from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from alfa_romeo_web.accounts.managers import AlfaRomeoUserManager
from alfa_romeo_web.accounts.validators import validate_profile_first_last_name, validate_profile_phone_number, \
    validate_past_date, validate_profile_picture_url


class AlfaRomeoUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    # password comes from `AbstractBaseUser`
    # last_login comes from `AbstractBaseUser`

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        editable=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "email"

    objects = AlfaRomeoUserManager()

    class Meta:
        verbose_name_plural = "Alfa Romeo Website Users"


class Profile(models.Model):
    MAX_FIRST_NAME_LENGTH = 30
    MIN_FIRST_NAME_LENGTH = 2
    MAX_LAST_NAME_LENGTH = 30
    MIN_LAST_NAME_LENGTH = 2
    MAX_PHONE_NUMBER_LENGTH = 14

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        validators=(
            validate_profile_first_last_name,
            MinLengthValidator(MIN_FIRST_NAME_LENGTH),
        ),
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        validators=(
            validate_profile_first_last_name,
            MinLengthValidator(MIN_LAST_NAME_LENGTH),
        ),
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        validators=(
            validate_past_date,
        )
    )

    phone_number = models.CharField(
        max_length=14,
        validators=(
            validate_profile_phone_number,
        ),
        blank=True,
        null=True,
    )

    profile_picture = models.URLField(
        blank=True,
        null=True,
        validators=(
            validate_profile_picture_url,
        )
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    user = models.OneToOneField(
        AlfaRomeoUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return self.first_name or self.last_name
