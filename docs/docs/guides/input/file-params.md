# 文件上传

处理文件与处理其他参数没有区别。

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` 是 [Django's UploadFile](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile) 的别名，它具有访问上传文件的所有方法和属性。

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - 等

## 上传多个文件

要同时**上传多个文件**，只需声明一个`List` 在 `UploadedFile`中:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## 上传带有额外字段的文件
注意：HTTP 协议默认情况下不允许您以 `application/json` 格式发送文件（除非您在客户端对其进行某种 JSON 编码）

要发送带有一些额外属性的文件，您需要使用 `multipart/form-data` 编码发送正文。您可以通过简单地将字段标记为 `Form` 来实现：

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

注意：在这种情况下，所有字段都应作为表单字段发送

您也可以将有效负载作为单个字段以 JSON 形式发送 - 只需从以下位置删除 `Form` 标记：


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

这将期望客户端以带有 2 个字段的 `multipart/form-data `发送数据：
  
  - details: 作为字符串的JSON
  - file: 文件


### 带有额外信息的文件列表

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
