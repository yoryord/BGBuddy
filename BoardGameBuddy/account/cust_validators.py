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




# @deconstructible
# class RangeValidatorFloatInclusive:
#     def __init__(self,  min_value: float, max_value: float):
#         self.min_value = min_value
#         self.max_value = max_value
#
#     def __call__(self, value):
#         if value < self.min_value or value > self.max_value:
#             raise ValidationError(f'The rating must be between {self.min_value:.2f} and {self.max_value:.2f}.')
#
#     def __eq__(self, other):
#         if not isinstance(other, self.__class__):
#             return NotImplemented
#         return (
#                 self.min_value == other.min_value
#                 and self.max_value == other.max_value
#         )



