# How-to guides

This part of the project documentation focuses on a
**problem-oriented** approach. You'll tackle common
tasks that you might have, with the help of the code
provided in this project.

## Ready-to-use classes

Consider the scenario below:

```python
import upload_to
from django.db import models


class MyUser(models.Model):
    username = models.CharField(...)
    avatar = models.FileField(upload_to=<generator>)

instance = MyUser(username='user@email.com')
```

Replace the `<generator>` fragment by the generators as showed below:

### Folder name

File in root folder

```python
>>> generator = upload_to.UploadTo()
>>> generator(instance, "file.pdf")
"file.pdf"
```

Subfolders

```python
>>> generator = upload_to.UploadTo(prefix=["files", "documents"])
>>> generator(instance, "file.pdf")
"files/documents/file.pdf"
```
Folder name from datetime

```python
>>> generator = upload_to.UploadTo(prefix=["pictures", "%Y"])
>>> generator(instance, "file.png")
"pictures/2023/file.png"
```

Using the instance's attributes

```python
>>> generator = upload_to.AttrUploadTo(attrs=["username"])
>>> generator(instance, "file.pdf")
"useremailcom/file.pdf"
```

Using the app_label and the model_name

```python
>>> generator = upload_to.ModelUploadTo()
>>> generator(instance, "file.pdf")
"my_app/user/file.pdf"
```

### File name

Using hexadecimal uuid value
```python
# 4. replace file name by a uuid value
>>> generator = upload_to.UuidUploadTo()
>>> generator(instance, "file.pdf")
"b189dfdf25e640b2ba5c497472c20962.pdf"
```

Normalize file name

```python
>>> generator = upload_to.UploadTo()
>>> generator(instance, "Á File_namE.pdf")
"a-file-name.pdf"
```

## Function generator

The function generator follows the Django's pattern using two arguments: instance and filename, and returns a str containing the path and file name.
You must follow this pattern too.

```python
# my_app/models.py
import upload_to
from django.db import models


def my_upload_generator(instance, filename):
    filename = upload_to.uuid_filename(filename)
    path = upload_to.options_from_instance(instance)
    return upload_to.upload_to(path, filename)

class MyProfile(models.Model):
    user = models.OneToOneField(...)
    avatar = models.FileField(upload_to=my_upload_generator)
```