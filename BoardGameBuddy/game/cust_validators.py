from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class YearRangeValidator:

    def __init__(self, min_year, max_year, message):
        self.min_year = min_year
        self.max_year = max_year
        self.message = message

    def __call__(self, value):
        if value < self.min_year or value > self.max_year:
            raise ValidationError(self.message)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
                self.min_year == other.min_year
                and self.max_year == other.max_year
        )


def validate_title_chars(value):
    for chr in value:
        if not chr.isalnum() and chr != ":" and chr != " ":
            raise ValidationError("Title should contain only letters, numbers and colon (:).")


def validate_first_capital_letter_of_title(value):
    if not value[0].isupper():
        raise ValidationError("Title should start with a capital letter.")

def validate_publisher_chars(value):
    for chr in value:
        if not chr.isalnum() and chr != "." and chr != " ":
            raise ValidationError("Only letters, numbers and dots (.) are allowed.")