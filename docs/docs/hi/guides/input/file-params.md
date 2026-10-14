---
comments: true
---
# File Uploads

Files को संभालना अन्य parameters को संभालने से कोई अलग नहीं है।

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile`, [Django के UploadFile](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile) का एक alias है, जिसमें uploaded file तक पहुँचने के सभी methods और attributes होते हैं।

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - आदि।

## एक साथ कई Files upload करना

एक साथ **कई files upload करने** के लिए, बस `UploadedFile` की एक `List` घोषित करें:


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## अतिरिक्त Fields के साथ Files upload करना
Note: HTTP protocol डिफ़ॉल्ट रूप से `application/json` format में files भेजने की अनुमति नहीं देता (जब तक कि आप client side पर कुछ JSON encoding न करें)।

किसी file को कुछ अतिरिक्त गुणों के साथ भेजने के लिए, आपको body को `multipart/form-data` encoding के साथ भेजना होगा। आप इसे बस fields को `Form` के रूप में चिह्नित करके कर सकते हैं:

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

Note: इस स्थिति में, सभी fields को form fields के रूप में भेजा जाना चाहिए।

आप payload को एक single JSON field के रूप में भी भेज सकते हैं — बस `Form` मार्कर हटा दें:


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

इससे यह अपेक्षा की जाएगी कि client data को `multipart/form-data` के रूप में 2 fields के साथ भेजे:

  - details: string के रूप में JSON
  - file: वह file


### अतिरिक्त जानकारी के साथ Files की List

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    अगले अध्याय पर जाएँ! **[Request Parsers](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
