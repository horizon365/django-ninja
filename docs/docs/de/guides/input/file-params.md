---
comments: true
---
# Datei-Uploads

Der Umgang mit Dateien unterscheidet sich nicht vom Umgang mit anderen Parametern.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` ist ein Alias für [Djangos UploadFile](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile), der alle Methoden und Attribute für den Zugriff auf die hochgeladene Datei bereitstellt.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - usw.

## Mehrere Dateien hochladen

Um **mehrere Dateien auf einmal hochzuladen**, deklarieren Sie einfach eine `List` von `UploadedFile`:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## Dateien mit zusätzlichen Feldern hochladen
Hinweis: Das HTTP-Protokoll erlaubt es standardmäßig nicht, Dateien im Format `application/json` zu senden (sofern Sie clientseitig keine JSON-Kodierung durchführen).

Um eine Datei zusammen mit zusätzlichen Eigenschaften zu senden, müssen Sie den Body mit der Kodierung `multipart/form-data` senden. Das können Sie ganz einfach erreichen, indem Sie die Felder als `Form` markieren:

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

Hinweis: In diesem Fall sollten alle Felder als Formularfelder gesendet werden.

Sie können die Nutzdaten auch als einzelnes JSON-Feld senden – entfernen Sie dafür einfach die `Form`-Markierung:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

Dann erwartet die API, dass der Client die Daten als `multipart/form-data` mit 2 Feldern sendet:
  
  - details: JSON als String
  - file: die Datei


### Eine Liste von Dateien mit zusätzlichen Informationen

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    Weiter zum nächsten Kapitel! **[Request-Parser](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
