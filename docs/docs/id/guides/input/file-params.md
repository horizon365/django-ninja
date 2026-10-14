---
comments: true
---
# Upload File

Penanganan file tidak berbeda dengan penanganan parameter lainnya.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` adalah alias untuk [UploadFile milik Django](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile), yang memiliki semua method dan atribut untuk mengakses file yang diunggah.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - dll.

## Mengunggah Beberapa File Sekaligus

Untuk **mengunggah beberapa file** sekaligus, cukup deklarasikan sebuah `List` dari `UploadedFile`:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## Mengunggah File dengan Field Tambahan
Catatan: Protokol HTTP secara default tidak mengizinkan Anda mengirim file dalam format `application/json` (kecuali Anda melakukan beberapa encoding JSON di sisi client).

Untuk mengirim file beserta beberapa properti tambahan, Anda perlu mengirim body menggunakan encoding `multipart/form-data`. Anda dapat melakukannya dengan mudah dengan menandai field sebagai `Form`:

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

Catatan: dalam kasus ini, semua field harus dikirim sebagai form fields.

Anda juga dapat mengirim payload sebagai satu field JSON — cukup hapus penanda `Form`:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

Ini akan mengharapkan client mengirim data sebagai `multipart/form-data` dengan 2 field:
  
  - details: JSON berupa string
  - file: file-nya


### Daftar File dengan Informasi Tambahan

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    Lanjutkan ke bab berikutnya! **[Request Parsers](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
