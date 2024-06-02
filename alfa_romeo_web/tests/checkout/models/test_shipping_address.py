from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from alfa_romeo_web.checkout.models import ShippingAddress

UserModel = get_user_model()


class ShippingAddressTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(email='test@example.com')

    def test_valid_shipping_address(self):
        shipping_address = ShippingAddress(
            user=self.user,
            shipping_address='street address',
            shipping_address_two='street address',
            country='Bulgaria',
            town='Sofia',
            zip='1000'
        )
        shipping_address.full_clean()

    def test_invalid_shipping_address_length(self):
        shipping_address = ShippingAddress(
            user=self.user,
            shipping_address='str',
            shipping_address_two='street address',
            country='Bulgaria',
            town='Sofia',
            zip='1000'
        )

        with self.assertRaises(ValidationError) as context:
            shipping_address.full_clean()

        self.assertEqual("['Ensure this value has at least 5 characters (it has 3).']",
                         str(context.exception.error_dict['shipping_address'][0]))

        print(str(context.exception))
