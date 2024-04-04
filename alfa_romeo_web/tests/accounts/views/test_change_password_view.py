from django.urls import reverse
from django.test import TestCase

from alfa_romeo_web.accounts.models import AlfaRomeoUser, Profile


class ProfileChangePasswordViewTest(TestCase):
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

    def test_profile_change_password_view(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        response = self.client.get(reverse('password-change', kwargs={'pk': profile.pk}))

        self.assertEqual(response.status_code, 302)
        print(response.status_code)

        redirected_response = self.client.get(response.url)
        print(redirected_response)

        response = self.client.post(reverse('password-change', kwargs={'pk': profile.pk}), {
            'old_password': 'Test1234',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

        self.assertEqual(response.status_code, 302)