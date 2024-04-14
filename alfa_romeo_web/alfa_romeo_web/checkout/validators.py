from django.core.exceptions import ValidationError


def validate_no_digits(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('The value cannot contain numeric digits.')