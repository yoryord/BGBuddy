from django.core.exceptions import ValidationError


def validate_file_size(image_object):
    if image_object.size > 1048576:
        raise ValidationError('The maximum file size is 1MB.')

