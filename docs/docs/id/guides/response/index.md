---
comments: true
---
# Response Schema

**Django Ninja** memungkinkan Anda mendefinisikan response schemas untuk keperluan validasi dan dokumentasi.

Bayangkan Anda perlu membuat sebuah operasi API yang membuat user. Parameter **input**-nya adalah **username+password**, tetapi **output** dari operasi ini seharusnya **id+username** (**tanpa** password).

Mari kita buat input schema-nya:

```python hl_lines="3 5"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


@api.post("/users/")
def create_user(request, data: UserIn):
    user = User(username=data.username) # User class comes from django auth.User
    user.set_password(data.password)
    user.save()
    # ... return ?
```

Sekarang mari kita definisikan output schema-nya dan meneruskannya sebagai argumen `response` ke decorator `@api.post`:

```python hl_lines="8 9 10 13 18"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


class UserOut(Schema):
    id: int
    username: str


@api.post("/users/", response=UserOut)
def create_user(request, data: UserIn):
    user = User(username=data.username)
    user.set_password(data.password)
    user.save()
    return user
```

**Django Ninja** akan menggunakan schema `response` untuk:

- Mengonversi data output ke schema yang dideklarasikan
- Memvalidasi data
- Menambahkan definisi skema OpenAPI
- Skema tersebut akan digunakan oleh sistem dokumentasi otomatis
- Dan, yang paling penting, skema tersebut akan **membatasi data output** hanya pada field yang didefinisikan dalam schema.

## Nested Objects

Hal yang juga umum adalah kebutuhan untuk mengembalikan response dengan beberapa nested/sub-objects.

Bayangkan kita memiliki Django model `Task` dengan foreign key `User`:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

Sekarang mari kita keluarkan semua tasks dan, untuk setiap task, keluarkan beberapa field tentang user-nya.

```python hl_lines="13 16"
from typing import List
from ninja import Schema

class UserSchema(Schema):
    id: int
    first_name: str
    last_name: str

class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: UserSchema = None  # ! None - the marker makes it non-required


@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    queryset = Task.objects.select_related("owner")
    return list(queryset)
```

Jika Anda mengeksekusi operasi ini, Anda akan mendapatkan response seperti ini:

```JSON hl_lines="6 7 8 9 16"
[
    {
        "id": 1,
        "title": "Task 1",
        "is_completed": false,
        "owner": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
        }
    },
    {
        "id": 2,
        "title": "Task 2",
        "is_completed": false,
        "owner": null
    },
]
```

## Aliases

Alih-alih menggunakan response nested, Anda mungkin ingin meratakan (flatten) output response saja.
Objek `Schema` milik Ninja memperluas format `Field(..., alias="")` Pydantic untuk menangani response bertitik.

Menggunakan model di atas, mari kita buat schema yang hanya menyertakan first name pemilik task secara inline, dan juga menggunakan `completed` alih-alih `is_completed`:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Aliases juga mendukung akses variabel dengan sintaks template Django:

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable will be executed
```

## Resolvers

Anda juga dapat membuat computed fields melalui resolver methods berdasarkan nama field.

Method tersebut harus menerima satu argumen, yaitu objek yang sedang di-resolve oleh schema.

Saat membuat resolver sebagai method standar, `self` memberi Anda akses ke atribut-atribut lain yang telah divalidasi dan diformat dalam schema.

```python hl_lines="5 7-11"
class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: Optional[str] = None
    lower_title: str

    @staticmethod
    def resolve_owner(obj):
        if not obj.owner:
            return
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def resolve_lower_title(self, obj):
        return self.title.lower()
```

### Mengakses Extra Context

Pydantic v2 memungkinkan Anda menangani extra context yang diteruskan ke serializer. Dalam contoh berikut, Anda dapat memiliki resolver yang mengambil objek request dari argumen `context` yang diteruskan:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

Jika Anda menggunakan schema ini untuk request yang masuk — objek request akan otomatis diteruskan ke context.

Anda juga dapat meneruskan context Anda sendiri:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Mengembalikan Queryset

Pada contoh sebelumnya, kita sengaja mengonversi queryset menjadi list (dan mengeksekusi query SQL saat evaluasi).

Anda dapat menghindari hal tersebut dan mengembalikan queryset sebagai hasilnya, dan queryset akan otomatis dievaluasi menjadi list:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    Jika operasi Anda asinkron, contoh ini tidak akan berfungsi, karena query ORM perlu dipanggil secara aman.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    Untuk informasi lebih lanjut, lihat [Async Support](../async-support.md#using-orm) .

## File Fields dan Image Fields

**Django Ninja** mengubah file dan gambar (yang dideklarasikan menggunakan `FileField` atau `ImageField`) menjadi URL `string` secara default.

Sebuah contoh:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

Jika Anda perlu mengeluarkan image field ke response, deklarasikan schema untuknya seperti ini:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

Setelah Anda mengeluarkannya ke response, sebuah URL akan otomatis dibuat untuk setiap objek:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Beberapa Response Schemas

Terkadang Anda perlu mendefinisikan beberapa response schemas.

Misalnya, dalam kasus autentikasi, Anda mungkin mengembalikan:

- **200** sukses -> token
- **401** -> Unauthorized
- **402** -> Payment required
- dll.

Faktanya, [spesifikasi OpenAPI](https://swagger.io/docs/specification/describing-responses/) memungkinkan Anda meneruskan beberapa response schemas.

Anda dapat meneruskan sebuah dictionary ke argumen `response`, di mana:

- keys-nya adalah response codes
- values-nya adalah schema untuk masing-masing code

Selain itu, ketika Anda mengembalikan hasilnya — Anda juga harus meneruskan sebuah status code untuk memberi tahu **Django Ninja** schema mana yang harus digunakan untuk validasi dan serialisasi.

Sebuah contoh:

```python hl_lines="9 12 14 16"
class Token(Schema):
    token: str
    expires: date

class Message(Schema):
    message: str


@api.post('/login', response={200: Token, 401: Message, 402: Message})
def login(request, payload: Auth):
    if auth_not_valid:
        return 401, {'message': 'Unauthorized'}
    if negative_balance:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': xxx, ...}
```

## Beberapa Response Codes

Pada contoh sebelumnya, Anda melihat bahwa kita pada dasarnya mengulang schema `Message` dua kali:

```
...401: Message, 402: Message}
```

Untuk menghindari duplikasi ini, Anda dapat menggunakan beberapa response codes untuk satu schema:

```python hl_lines="2 5 8 10"
...
from ninja.responses import codes_4xx


@api.post('/login', response={200: Token, codes_4xx: Message})
def login(request, payload: Auth):
    if auth_not_valid:
        return 401, {'message': 'Unauthorized'}
    if negative_balance:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': xxx, ...}
```

**Django Ninja** dilengkapi dengan HTTP codes berikut:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

Anda juga dapat membuat rentang Anda sendiri menggunakan `frozenset`:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## Response Kosong

Beberapa response, seperti [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), tidak memiliki body.
Untuk menandakan bahwa response body kosong, tandai argumen `response` dengan `None` alih-alih sebuah schema:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Error Responses

Untuk informasi lebih lanjut, lihat [Penanganan Error](../errors.md) .

## Self-referencing Schemes

- Terkadang Anda perlu membuat schema yang mereferensikan dirinya sendiri atau objek berbentuk pohon (tree-like).

- Untuk melakukannya, Anda perlu:

- membungkus tipe schema Anda dengan tanda kutip

- menggunakan method `update_forward_refs` untuk menerapkan tipe yang mereferensikan dirinya sendiri

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## Self-referencing Schemes yang Dihasilkan dari `create_schema()`

Agar dapat menggunakan method `update_forward_refs()` dari schema yang dihasilkan melalui `create_schema()`,
"name" dari class tersebut perlu berada di namespace kita. Dalam kasus ini, penting untuk meneruskan argumen `name` ke `create_schema()`.

```python hl_lines="3"
UserSchema = create_schema(
    User,
    name='UserSchema',  # !!! this is important for update_forward_refs()
    fields=['id', 'username']
    custom_fields=[
        ('manager', 'UserSchema', None),
    ]
)
UserSchema.update_forward_refs()
```

## Serialisasi di Luar View

Anda dapat langsung melakukan serialisasi objek Anda dalam kode menggunakan method `.from_orm()` pada objek schema.

Perhatikan model berikut:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

Model tersebut dapat diakses menggunakan schema berikut:
```python
class PersonSchema(Schema):
    name: str
```

Serialisasi dapat dilakukan langsung menggunakan method `.from_orm()` pada schema.
Setelah Anda memiliki instance dari objek schema tersebut, method `.dict()` dan `.json()` memungkinkan Anda mendapatkan output dictionary dan versi JSON berupa string.

```python
>>> person = Person.objects.get(id=1)
>>> data = PersonSchema.from_orm(person)
>>> data
PersonSchema(id=1, name='Mr. Smith')
>>> data.dict()
{'id':1, 'name':'Mr. Smith'}
>>> data.json()
'{"id":1, "name":"Mr. Smith"}'
```

Beberapa entri: atau sebuah queryset (atau list)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django HTTP Responses

Anda juga dapat mengembalikan HTTP response Django biasa:

```python
from django.http import HttpResponse
from django.shortcuts import redirect


@api.get("/http")
def result_django(request):
    return HttpResponse('some data')   # !!!!


@api.get("/something")
def some_redirect(request):
    return redirect("/some-path")  # !!!!
```

!!! done

    Lanjutkan ke bab berikutnya! **[Tweaking the Response](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
