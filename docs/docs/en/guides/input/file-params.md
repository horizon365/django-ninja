---
comments: true
---
# File Uploads

Handling files is no different from handling other parameters.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` is an alias for [Django's UploadFile](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile), which has all the methods and attributes for accessing the uploaded file.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - etc.

## Uploading Multiple Files

To **upload multiple files** at once, simply declare a `List` of `UploadedFile`:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## Uploading Files with Extra Fields
Note: The HTTP protocol does not allow you to send files in `application/json` format by default (unless you perform some JSON encoding on the client side).

To send a file with some additional properties, you need to send the body using `multipart/form-data` encoding. You can do this simply by marking the fields as `Form`:

```python hl_lines="14"
from ninja import NinjaAPI, Schema, UploadedFile, Form, File
from datetime import date

api = NinjaAPI()


class UserDetails(Schema):
    first_name: str
    last_name: str
    birthdate: date


@api.post('/users')
def create_user(request, details: Form[UserDetails], file: File[UploadedFile]):
    return [details.dict(), file.name]

```

Note: in this case, all fields should be sent as form fields.

You can also send the payload as a single JSON field — just remove the `Form` marker:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

This will expect the client to send the data as `multipart/form-data` with 2 fields:
  
  - details: JSON as a string
  - file: the file


### A List of Files with Extra Information

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    Continue to the next chapter! **[Request Parsers](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
