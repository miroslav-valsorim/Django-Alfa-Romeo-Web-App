from django.forms import DateInput
from django.test import TestCase, RequestFactory
from django.urls import reverse

from alfa_romeo_web.accounts.models import AlfaRomeoUser, Profile
from alfa_romeo_web.accounts.views import ProfileEditView


class TestProfileEditView(TestCase):
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

    def test_profile_edit_view(self):
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        response = self.client.get(reverse('edit-profile', kwargs={'pk': profile.pk}))

        self.assertEqual(response.status_code, 302)
        print(response.status_code)

        redirected_response = self.client.get(response.url)
        print(redirected_response)

        self.assertEqual(redirected_response.status_code, 200)

    def test_get_success_url(self):
        view = ProfileEditView()
        profile = self.create_profile(self.VALID_PROFILE_DATA)
        view.object = profile
        self.assertEqual(view.get_success_url(), reverse('details-profile', kwargs={'pk': profile.pk}))

    def test_get_form(self):
        view = ProfileEditView()

        request = RequestFactory().get('/fake-url/')
        view.request = request

        form = view.get_form()
        self.assertIsInstance(form.fields["first_name"].widget.attrs, dict)
        self.assertEqual(form.fields["first_name"].label, "First Name")
        self.assertIsInstance(form.fields["last_name"].widget.attrs, dict)
        self.assertEqual(form.fields["last_name"].label, "Last Name")
        self.assertIsInstance(form.fields["date_of_birth"].widget, DateInput)
        self.assertEqual(form.fields["date_of_birth"].label, "Birthday")
        self.assertIsInstance(form.fields["phone_number"].widget.attrs, dict)
        self.assertEqual(form.fields["phone_number"].label, "Phone Number")
        self.assertIsInstance(form.fields["profile_picture"].widget.attrs, dict)
        self.assertEqual(form.fields["profile_picture"].label, "Profile Picture")