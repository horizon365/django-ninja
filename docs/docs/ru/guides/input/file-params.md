---
comments: true
---
# Загрузка файлов

Обработка файлов ничем не отличается от обработки других параметров.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` — это псевдоним для [UploadFile из Django](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile), который предоставляет все методы и атрибуты для доступа к загруженному файлу.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - и т. д.

## Загрузка нескольких файлов

Чтобы **загрузить несколько файлов** одновременно, просто объявите `List` из `UploadedFile`:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## Загрузка файлов с дополнительными полями
Примечание: протокол HTTP по умолчанию не позволяет отправлять файлы в формате `application/json` (если только вы не выполняете какое-либо JSON-кодирование на стороне клиента).

Чтобы отправить файл вместе с дополнительными свойствами, нужно отправить тело в кодировке `multipart/form-data`. Это легко сделать, пометив поля как `Form`:

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

Примечание: в этом случае все поля должны отправляться как поля формы.

Вы также можете отправить данные как одно JSON-поле — просто уберите маркер `Form`:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

В этом случае от клиента ожидается отправка данных в формате `multipart/form-data` с двумя полями:
  
  - details: JSON в виде строки
  - file: файл


### Список файлов с дополнительной информацией

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    Переходите к следующей главе! **[Парсеры запросов](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
