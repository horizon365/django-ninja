---
comments: true
---
# 파일 업로드

파일 처리는 다른 파라미터를 처리하는 것과 다르지 않습니다.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile`은 [Django의 UploadFile](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile)의 별칭으로, 업로드된 파일에 접근하기 위한 모든 메서드와 속성을 가지고 있습니다.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - etc.

## 여러 파일 업로드

한 번에 **여러 파일을 업로드**하려면 `UploadedFile`의 `List`를 선언하기만 하면 됩니다:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## 추가 필드와 함께 파일 업로드
참고: HTTP 프로토콜은 기본적으로 `application/json` 형식으로 파일을 전송하는 것을 허용하지 않습니다(클라이언트 측에서 일부 JSON 인코딩을 수행하는 경우는 예외).

파일에 추가 속성을 담아 전송하려면, body를 `multipart/form-data` 인코딩으로 보내야 합니다. 필드를 `Form`으로 마킹하기만 하면 간단히 이를 수행할 수 있습니다:

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

참고: 이 경우 모든 필드는 폼 필드로 전송되어야 합니다.

페이로드를 단일 JSON 필드로 보낼 수도 있습니다 - `Form` 마커만 제거하면 됩니다:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

이 경우 클라이언트는 2개의 필드로 구성된 `multipart/form-data`로 데이터를 보내야 합니다:
  
  - details: 문자열 형태의 JSON
  - file: 파일


### 추가 정보와 함께 파일 리스트 업로드

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    다음 챕터로 계속 진행하세요! **[Request Parsers](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
