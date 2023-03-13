from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def validate_new_password(password):
    try:
        validate_password(password)
    except ValidationError as e:
        return e