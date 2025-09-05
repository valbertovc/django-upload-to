from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible

__all__ = [
    "MaxSizeValidator",
    "MinSizeValidator",
    "KB",
    "MB",
    "GB",
    "TB",
    "PB",
]

KB = 1 << 10
MB = 1 << 20
GB = 1 << 30
TB = 1 << 40
PB = 1 << 50


@deconstructible
class BaseFileValidator(BaseValidator):
    def __call__(self, value):
        """
        This method was overridden only to be able to pass the
        filesize formatted unit parameter in the exception raising.
        Its logic follows exactly what Django does in the BaseValidator class.
        """
        cleaned = self.clean(value)
        limit_value = (
            self.limit_value() if callable(self.limit_value) else self.limit_value
        )
        params = {
            "limit_value": filesizeformat(limit_value),
            "show_value": filesizeformat(cleaned),
            "value": value,
        }
        if self.compare(cleaned, limit_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def clean(self, x):
        return x.size


@deconstructible
class MaxSizeValidator(BaseFileValidator):
    message = (
        "Ensure this file size is less than %(limit_value)s "
        "(current size: %(show_value)s)."
    )
    code = "max_file_size"

    def compare(self, a, b):
        return a > b


@deconstructible
class MinSizeValidator(BaseFileValidator):
    message = (
        "Ensure this file size is greater than %(limit_value)s "
        "(current size: %(show_value)s)."
    )
    code = "min_file_size"

    def compare(self, a, b):
        return a < b
