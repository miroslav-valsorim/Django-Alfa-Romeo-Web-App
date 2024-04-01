from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_profile_first_last_name(name):
    if not name[0].isalpha() or not name[0].isupper():
        raise ValidationError('Both First and Last names should start with capital letter!')
    for ch in name:
        if not ch.isalpha():
            raise ValidationError('Names should contain only letters!')


def validate_profile_phone_number(phone_number):
    if not phone_number.startswith('+359') and not phone_number.startswith('0'):
        raise ValidationError(
            _('Phone number must start with +359 or 0.')
        )

    if phone_number.startswith('+359') and len(phone_number) != 14:
        raise ValidationError(
            _('If the phone number starts with +359, the length of number should be 14.')
        )

    if phone_number.startswith('0') and len(phone_number) != 10:
        raise ValidationError(
            _('If the phone number starts with 0, the length of number should be 10.')
        )
