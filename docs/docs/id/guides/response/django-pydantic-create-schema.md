---
comments: true
---
# Menghasilkan Schema Secara Dinamis

Di balik layar, [`ModelSchema`](django-pydantic.md#modelschema) menggunakan fungsi `create_schema`.
Ini adalah pendekatan yang lebih lanjut (dan kurang aman) — gunakan dengan hati-hati.

## `create_schema`

**Django Ninja** dilengkapi dengan fungsi helper `create_schema`:

```python
def create_schema(
    model, # django model
    name = "", # name for the generated class, if empty model names is used
    depth = 0, # if > 0 schema will also be created for the nested ForeignKeys and Many2Many (with the provided depth of lookup)
    fields: list[str] = None, # if passed - ONLY these fields will added to schema
    exclude: list[str] = None, # if passed - these fields will be excluded from schema
    optional_fields: list[str] | str = None, # if passed - these fields will not be required on schema (use '__all__' to mark ALL fields required)
    custom_fields: list[tuple(str, Any, Any)] = None, # if passed - this will override default field types (or add new fields)
)
```


Perhatikan contoh berikut:

```python hl_lines="2 4"
from django.contrib.auth.models import User
from ninja.orm import create_schema

UserSchema = create_schema(User)

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     password: str
#     last_login: datetime
#     is_superuser: bool
#     email: str
#     ... and the rest

```

!!! warning
    Secara default, `create_schema` membangun schema menggunakan semua field model.
    Hal ini dapat menyebabkan terexposnya data yang tidak diinginkan secara tidak sengaja (seperti password yang di-hash, pada contoh di atas).
    <br>
    **Selalu** gunakan argumen `fields` atau `exclude` untuk mendefinisikan daftar atribut secara eksplisit.

### Menggunakan `fields`

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### Menggunakan `exclude`

```python hl_lines="1 2"
UserSchema = create_schema(User, exclude=[
    'password', 'last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions']
)

# Will create schema without excluded fields:
# 
# class UserSchema(Schema):
#    id: int
#    username: str
#    first_name: str
#    last_name: str
#    email: str
#    is_active: bool
#    date_joined: datetime
```

### Menggunakan `depth`

Argumen `depth` memungkinkan Anda meng-introspeksi field terkait dari Django model (foreign keys, one-to-one, many-to-many).

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

Perhatikan bahwa di sini groups menjadi `List[Group]` — field many-to-many di-introspeksi 1 level ke dalam dan schema juga dibuat untuk groups:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    Lanjutkan ke bab berikutnya! **[Meng-override Konfigurasi Pydantic](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
