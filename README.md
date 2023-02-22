# django-upload-to

[![codecov](https://codecov.io/github/valbertovc/django-upload-to/branch/main/graph/badge.svg?token=2R5S5GTS0X)](https://codecov.io/github/valbertovc/django-upload-to)

It generates dynamically a directory path and a secure file name for Django FileField.

Main options:
- File name more secures with dropping especial characters or replacing it by a uuid string.
- Flexible paths dynamically generate from model instance.
- Auto generate paths from Python datetime formats.

## How to use

```python
# my_app/models.py
from upload_to import UploadTo
from django.db import models


class MyModel(models.Model):
    attachment = models.FileField(upload_to=UploadTo())
```

## Examples

```python
import upload_to
from django.db import models


class MyUser(models.Model):
    username = models.CharField(...)


instance = MyUser(username='user@email.com')

# 1. root folder
>>> generator = upload_to.UploadTo()
>>> generator(instance, "file.pdf")
"file.pdf"

# 2. folder path defined
>>> generator = upload_to.UploadTo(prefix=["files", "documents"])
>>> generator(instance, "file.pdf")
"files/documents/file.pdf"

# 3. folder path with datetime formats
>>> generator = upload_to.UploadTo(prefix=["pictures", "%Y"])
>>> generator(instance, "file.png")
"pictures/2023/file.png"

# 4. replace file name by a uuid value
>>> generator = upload_to.UuidUploadTo()
>>> generator(instance, "file.pdf")
"b189dfdf25e640b2ba5c497472c20962.pdf"

# 5. replace folder path using instance's attributes
>>> generator = upload_to.AttrUploadTo(attrs=["username"])
>>> generator(instance, "file.pdf")
"useremailcom/file.pdf"

# 6. add the app_label and the model_name as folder path using 
#    instance's meta options
>>> generator = upload_to.ModelUploadTo()
>>> generator(instance, "file.pdf")
"my_app/user/file.pdf"
```

## Customize your upload paths

```python
# my_app/models.py
import upload_to


def my_upload_generator(instance, filename):
    filename = upload_to.uuid_filename(filename)
    path = upload_to.options_from_instance(instance)
    return upload_to.upload_to(path, filename)
```