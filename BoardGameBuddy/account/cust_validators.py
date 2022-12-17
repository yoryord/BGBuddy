from django.core.exceptions import ValidationError


def validate_file_size(image_object):
    if image_object.size > 1048576:
        raise ValidationError('The maximum file size is 1MB.')


def validate_nickname_chars(value):
    for chr in value:
        if not chr.isalnum() and chr != '_':
            raise ValidationError("Ensure this value contains only letters, numbers, and underscore.")


def validate_names_chars(value):
    for chr in value:
        if not chr.isalnum():
            raise ValidationError("Names should contain only letters and numbers.")
