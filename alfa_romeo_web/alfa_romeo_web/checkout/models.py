from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class ShippingAddress(models.Model):
    MAX_SHIPPING_ADDRESS_LENGTH = 150
    MAX_COUNTRY_LENGTH = 150
    MAX_TOWN_LENGTH = 100
    MAX_ZIP_LENGTH = 50

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    shipping_address = models.CharField(
        max_length=MAX_SHIPPING_ADDRESS_LENGTH,
        blank=False,
        null=False,
    )

    shipping_address_two = models.CharField(
        max_length=MAX_SHIPPING_ADDRESS_LENGTH,
        blank=False,
        null=False,
    )

    country = models.CharField(
        max_length=MAX_COUNTRY_LENGTH,
        blank=False,
        null=False,
    )

    town = models.CharField(
        max_length=MAX_TOWN_LENGTH,
        blank=False,
        null=False,
    )

    zip = models.CharField(
        max_length=MAX_ZIP_LENGTH,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.user.email
