---
comments: true
---
# ファイルアップロード

ファイルの取り扱いは、他のパラメータの取り扱いと変わりません。

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` は [Django の UploadFile](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile) のエイリアスで、アップロードされたファイルにアクセスするためのすべてのメソッドと属性を備えています。

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - など

## 複数ファイルのアップロード

**複数のファイルを一度にアップロード**するには、単に `UploadedFile` の `List` を宣言します:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## 追加フィールド付きのファイルアップロード
注: HTTP プロトコルでは、デフォルトでは `application/json` 形式でファイルを送信できません（クライアント側で何らかの JSON エンコーディングを行わない限り）。

ファイルに追加のプロパティを付けて送信するには、`multipart/form-data` エンコーディングでボディを送信する必要があります。これは、フィールドを `Form` としてマークするだけで実現できます:

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

注: この場合、すべてのフィールドはフォームフィールドとして送信する必要があります。

ペイロードを単一の JSON フィールドとして送信することもできます — `Form` マーカーを削除するだけです:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

この場合、クライアントが 2 つのフィールドを持つ `multipart/form-data` としてデータを送信することを期待します:

  - details: 文字列としての JSON
  - file: ファイル


### 追加情報付きのファイルのリスト

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    次の章に進みましょう！ **[リクエストパーサー](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
