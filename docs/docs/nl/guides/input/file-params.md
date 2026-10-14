---
comments: true
---
# Bestandsuploads

Het afhandelen van bestanden verschilt niet van het afhandelen van andere parameters.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` is een alias voor [de UploadFile van Django](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile), die alle methoden en attributen heeft voor toegang tot het geüploade bestand.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - enz.

## Meerdere bestanden uploaden

Om **meerdere bestanden tegelijk** te uploaden, declareer je gewoon een `List` van `UploadedFile`:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## Bestanden uploaden met extra velden
Let op: het HTTP protocol staat standaard niet toe om bestanden in `application/json` formaat te versturen (tenzij je aan de clientzijde een JSON-encoding uitvoert).

Om een bestand te versturen met enkele aanvullende eigenschappen, moet je de body versturen met de encoding `multipart/form-data`. Dit doe je simpelweg door de velden te markeren met `Form`:

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

Let op: in dit geval moeten alle velden als formuliervelden worden verstuurd.

Je kunt de payload ook als één JSON veld versturen — verwijder gewoon de `Form` markering:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

Dit verwacht dat de client de data verstuurt als `multipart/form-data` met 2 velden:
  
  - details: JSON als string
  - file: het bestand


### Een lijst van bestanden met extra informatie

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    Ga verder naar het volgende hoofdstuk! **[Request Parsers](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
