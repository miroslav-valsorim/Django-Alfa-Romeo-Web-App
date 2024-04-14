from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from alfa_romeo_web.checkout.validators import validate_no_digits

UserModel = get_user_model()


class ShippingAddress(models.Model):
    MAX_SHIPPING_ADDRESS_LENGTH = 150
    MIN_SHIPPING_ADDRESS_LENGTH = 5
    MAX_COUNTRY_LENGTH = 30
    MIN_COUNTRY_LENGTH = 2
    MAX_TOWN_LENGTH = 30
    MIN_TOWN_LENGTH = 2
    MAX_ZIP_LENGTH = 30
    MIN_ZIP_LENGTH = 2

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    shipping_address = models.CharField(
        max_length=MAX_SHIPPING_ADDRESS_LENGTH,
        validators=(
            MinLengthValidator(MIN_SHIPPING_ADDRESS_LENGTH),
        ),
        blank=False,
        null=False,
    )

    shipping_address_two = models.CharField(
        max_length=MAX_SHIPPING_ADDRESS_LENGTH,
        validators=(
            MinLengthValidator(MIN_SHIPPING_ADDRESS_LENGTH),
        ),
        blank=False,
        null=False,
    )

    country = models.CharField(
        max_length=MAX_COUNTRY_LENGTH,
        validators=(
            MinLengthValidator(MIN_COUNTRY_LENGTH),
            validate_no_digits,
        ),
        blank=False,
        null=False,
    )

    town = models.CharField(
        max_length=MAX_TOWN_LENGTH,
        validators=(
            MinLengthValidator(MIN_TOWN_LENGTH),
            validate_no_digits,
        ),
        blank=False,
        null=False,
    )

    zip = models.CharField(
        max_length=MAX_ZIP_LENGTH,
        validators=(
            MinLengthValidator(MIN_ZIP_LENGTH),
        ),
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.user.email
