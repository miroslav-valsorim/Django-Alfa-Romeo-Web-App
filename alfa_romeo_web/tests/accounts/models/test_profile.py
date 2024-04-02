from django.core.exceptions import ValidationError
from django.test import TestCase

from alfa_romeo_web.accounts.models import Profile, AlfaRomeoUser


class TestProfile(TestCase):
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'phone_number': '0891231231',
        'date_of_birth': '2022-12-11',
        'profile_picture': 'https://example.com/image.jpg',
    }
    VALID_USER_DATA = {
        'email': 'test@mail.bg',
        'password': 'Test1234',
    }

    def create_profile(self, data, **kwargs):
        user = AlfaRomeoUser.objects.create(**self.VALID_USER_DATA)
        profile_data = {
            **data,
            **kwargs,
            'user': user,
        }

        return Profile(**profile_data)

    # TEST first_name

    def test_create__when_first_name_has_1_more_than_valid_characters__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, first_name='A' * Profile.MAX_FIRST_NAME_LENGTH + 'a')
        print(profile.first_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Ensure this value has at most 30 characters (it has 31).']",
                         str(context.exception.error_dict['first_name'][0]))

    def test_create__when_first_name_has_1_less_than_valid_characters__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, first_name='A' * (Profile.MIN_FIRST_NAME_LENGTH - 1))
        print(profile.first_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Ensure this value has at least 2 characters (it has 1).']",
                         str(context.exception.error_dict['first_name'][0]))

    def test_create__when_first_name_starts_with_lowercase_character__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, first_name='test')
        print(profile.first_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Both First and Last names should start with capital letter!']",
                         str(context.exception.error_dict['first_name'][0]))

    def test_create__when_first_name_contains_not_alpha_character__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, first_name='Test1')
        print(profile.first_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Names should contain only letters!']", str(context.exception.error_dict['first_name'][0]))

    # TEST last_name

    def test_create__when_last_name_has_1_more_than_valid_characters__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, last_name='A' * Profile.MAX_FIRST_NAME_LENGTH + 'a')
        print(profile.last_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Ensure this value has at most 30 characters (it has 31).']",
                         str(context.exception.error_dict['last_name'][0]))

    def test_create__when_last_name_has_1_less_than_valid_characters__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, last_name='A' * (Profile.MIN_LAST_NAME_LENGTH - 1))
        print(profile.last_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Ensure this value has at least 2 characters (it has 1).']",
                         str(context.exception.error_dict['last_name'][0]))

    def test_create__when_last_name_starts_with_lowercase_character__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, last_name='testov')
        print(profile.last_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Both First and Last names should start with capital letter!']",
                         str(context.exception.error_dict['last_name'][0]))

    def test_create__when_last_name_contains_not_alpha_character__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, last_name='Testov1')
        print(profile.last_name)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Names should contain only letters!']", str(context.exception.error_dict['last_name'][0]))

    # TEST phone_number

    def test_create__when_phone_has_1_more_than_valid_characters__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, phone_number='0' * Profile.MAX_PHONE_NUMBER_LENGTH + '1')
        print(profile.phone_number)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['If the phone number starts with 0, the length of number should be 10.']",
                         str(context.exception.error_dict['phone_number'][0]))
        self.assertEqual("['Ensure this value has at most 14 characters (it has 15).']",
                         str(context.exception.error_dict['phone_number'][1]))

    def test_create__when_phone_starts_with_different_character_than_zero__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, phone_number='1231231231')
        print(profile.phone_number)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Phone number must start with +359 or 0.']",
                         str(context.exception.error_dict['phone_number'][0]))

    def test_create__when_phone_contains_not_digit_character__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, phone_number='0123123123a')
        print(profile.phone_number)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Phone number should contain only numbers.']",
                         str(context.exception.error_dict['phone_number'][0]))

    # Test Date of Birth

    def test_create__when_date_of_birth_is_future__expect_to_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, date_of_birth='2024-12-12')
        print(profile.date_of_birth)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)
        self.assertEqual("['Date of birth cannot be a future date.']",
                         str(context.exception.error_dict['date_of_birth'][0]))

    def test_create__when_date_of_birth_is_valid__expect_no_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        print(profile.date_of_birth)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)

    # Test Profile Picture

    def test_create__when_profile_picture_is_not_url__expect_to_raise(self):
        with self.assertRaises(ValidationError) as context:
            self.create_profile(self.VALID_PROFILE_DATA, profile_picture='not_a_url').full_clean()
        self.assertTrue('profile_picture' in context.exception.error_dict)

    def test_create__when_profile_picture_is_valid_url__expect_no_raise(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        print(profile.date_of_birth)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
        print(context.exception)

    # Test Full Name Property

    def test_full_name_property_with_both_names(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        self.assertEqual(profile.full_name, 'Test Testov')

    def test_full_name_property_with_only_first_name(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, last_name='')
        self.assertEqual(profile.full_name, 'Test')

    def test_full_name_property_with_only_last_name(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, first_name='')
        self.assertEqual(profile.full_name, 'Testov')

    def test_full_name_property_with_no_names(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA, first_name='', last_name='')
        self.assertEqual(profile.full_name, '')

    def test_str_method(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        expected_str = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(str(profile), expected_str)
