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

## File size validation

### Limiting maximum file size

Use `MaxSizeValidator` to ensure uploaded files don't exceed a certain size:

```python
from upload_to import UploadTo, MaxSizeValidator, MB
from django.db import models


class Document(models.Model):
    file = models.FileField(
        upload_to=UploadTo("documents"),
        validators=[MaxSizeValidator(1 * MB)]  # Max 1MB
    )
```

### Setting minimum file size

Use `MinSizeValidator` to ensure uploaded files meet a minimum size requirement:

```python
from upload_to import UploadTo, MinSizeValidator, KB
from django.db import models


class Image(models.Model):
    photo = models.FileField(
        upload_to=UploadTo("photos"),
        validators=[MinSizeValidator(5 * KB)]  # Min 5KB
    )
```

### Combining size validators

You can use both validators together to define acceptable file size ranges:

```python
from upload_to import UploadTo, MaxSizeValidator, MinSizeValidator, KB, MB
from django.db import models


class Avatar(models.Model):
    image = models.FileField(
        upload_to=UploadTo("avatars"),
        validators=[
            MinSizeValidator(1 * KB),   # Min 1KB
            MaxSizeValidator(2 * MB),    # Max 2MB
        ]
    )
```

### Using callable limit values

Validators also support callable limit values for dynamic sizing:

```python
from upload_to import MaxSizeValidator, MB


def get_max_size():
    # Dynamic size based on user subscription level, etc.
    return 5 * MB


class UserFile(models.Model):
    file = models.FileField(
        validators=[MaxSizeValidator(get_max_size)]
    )
```

### Size unit constants

The library provides convenient constants for common file sizes:

- `KB` = 1,024 bytes (1 kilobyte)
- `MB` = 1,048,576 bytes (1 megabyte)  
- `GB` = 1,073,741,824 bytes (1 gigabyte)
- `TB` = 1,099,511,627,776 bytes (1 terabyte)
- `PB` = 1,125,899,906,842,624 bytes (1 petabyte)

Example usage:
```python
from upload_to import MaxSizeValidator, KB, MB, GB

# Different size limits
validators=[MaxSizeValidator(500 * KB)]  # 500KB
validators=[MaxSizeValidator(10 * MB)]   # 10MB
validators=[MaxSizeValidator(2 * GB)]    # 2GB
```