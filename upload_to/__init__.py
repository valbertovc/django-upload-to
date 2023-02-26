import os
import pathlib
import unicodedata
from uuid import uuid4

from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify

__version__ = "0.1.1"

__all__ = [
    "uuid_filename",
    "upload_to",
    "normalize_filename",
    "options_from_instance",
    "UploadTo",
    "UuidUploadTo",
    "AttrUploadTo",
    "ModelUploadTo",
]


def uuid_filename(filename) -> str:
    """
    It replaces the original file name by a uuid4
    hexadecimal and keep its original extension.
    """
    ext = pathlib.Path(filename).suffix
    return uuid4().hex + ext.lower()


def upload_to(path: list, filename: str) -> str:
    """
    It creates a full path to file inside the path structure as subfolders.

    You can use strftime format codes to build directories
    names dynamicaly from current time zone.
    https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    """
    path = os.path.join(*path, filename)
    return timezone.now().strftime(path)


def normalize_filename(filename: str) -> str:
    """
    It normalizes the file name avoiding unexpected characters.
    """
    filename = default_storage.get_valid_name(filename)
    filename = (
        unicodedata.normalize("NFKD", filename)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    return filename.lower()


def options_from_instance(instance: models.Model) -> tuple:
    """
    It gets the basic options (app_label and model_name) from a model instance
    in order to provide values to build a dynamic directory structure.
    """
    opts = instance._meta  # pylint: disable=protected-access
    return opts.app_label, opts.model_name


@deconstructible
class UploadTo:
    """
    It generates a full path to upload files using Django FileField.

    prefix:
    - empty (None) means no folder. The file will be saved in root directory.
    - string: folder name.
    - string with slashed: folder and subfolders structure.
    - list with strings: folder and subfolders structure.
    """

    def __init__(self, prefix=None):
        if prefix is None:
            prefix = []
        if isinstance(prefix, str):
            prefix = prefix.split("/")
        self.prefix = prefix

    def __call__(self, instance, filename):
        dirname = self.get_dirname(instance)
        filename = self.get_filename(filename)
        return upload_to(dirname, filename)

    def get_dirname(self, instance) -> list:  # pylint: disable=unused-argument
        return self.prefix

    def get_filename(self, filename) -> str:
        return normalize_filename(filename)


@deconstructible
class UuidUploadTo(UploadTo):
    """
    It generates a full path to upload files using Django FileField and
    replaces the original file name by a hexadecimal value.
    """

    def get_filename(self, filename):
        filename = uuid_filename(filename)
        return super().get_filename(filename)


@deconstructible
class AttrUploadTo(UploadTo):
    """
    It generates a full path to upload files using Django FileField and
    replaces the original file name by a hexadecimal value.

    prefix: managed by UploadTo super class
    attrs:
    - empty (None) means no attributes to interpolate.
    - string: sigle attribute name.
    - list with strings: multiple attributes to generate the
      folder structure dynamically.
    """

    def __init__(self, prefix=None, attrs=None):
        super().__init__(prefix)
        if attrs is None:
            attrs = []
        if isinstance(attrs, str):
            attrs = [attrs]
        self.attrs = attrs

    def get_attrs(self, instance) -> list:
        return [
            slugify(getattr(instance, attr))
            for attr in self.attrs
            if getattr(instance, attr) is not None
        ]

    def get_dirname(self, instance) -> list:
        dirname = super().get_dirname(instance)
        return dirname + self.get_attrs(instance)


@deconstructible
class ModelUploadTo(AttrUploadTo):
    """
    It generates a full path to upload files using Django FileField and
    adds folders and subfolders using app_label and model_name
    from instance.
    """

    def get_dirname(self, instance) -> list:
        prefix = self.prefix
        options = options_from_instance(instance)
        attrs = self.get_attrs(instance)
        return [*prefix, *options, *attrs]
