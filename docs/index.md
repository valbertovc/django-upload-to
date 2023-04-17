# Welcome to django-upload-to documentation

[![codecov](https://codecov.io/github/valbertovc/django-upload-to/branch/main/graph/badge.svg?token=2R5S5GTS0X)](https://codecov.io/github/valbertovc/django-upload-to)

This site contains the project documentation for the
`django-upload-to` project that is a django reusable app used in the
Django projects.

## Table of contents

1. [Tutorials](tutorials.md)
2. [How-To Guides](how-to-guides.md)
3. [Reference](reference.md)
4. [Explanation](explanation.md)

# Introduction

It generates dynamically a directory path and a secure file name for Django's `FileField`.

Main options:

- Ready to use generators.
- Generate secure file name without especial characters.
- Generate file name using a uuid value.
- Dynamically generate paths from the model instance.
- Generate paths using Python datetime formats.

## Get started
Install the django-upload-to in your virtual environment:
```bash
$ pip install django-upload-to
```
Import it in your models file and add it as a `upload_to` argument in the `FileField` 
```python
# my_app/models.py
from upload_to import UploadTo
from django.db import models


class MyModel(models.Model):
    attachment = models.FileField(upload_to=UploadTo("attachments"))
```
The path and file name generated will be like this:
```text
"attachments/the-file-name-uploaded.pdf"
```

## Useful links

1. [Documentation](https://valbertovc.github.io/django-upload-to/)
2. [Changelog](https://github.com/valbertovc/django-upload-to/releases)
3. [PyPi Page](https://pypi.org/project/django-upload-to/)
4. [Repository](https://github.com/valbertovc/django-upload-to)
5. [Bug Tracker](https://github.com/valbertovc/django-upload-to/issues)