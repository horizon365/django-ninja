---
comments: true
---
# Menghasilkan Schema dari Django Models


Schema sangat berguna untuk mendefinisikan aturan validasi dan response, tetapi terkadang Anda perlu me-refleksikan database models Anda ke dalam schema dan menjaga perubahannya tetap sinkron.
## ModelSchema

`ModelSchema` adalah base class khusus yang dapat secara otomatis menghasilkan schema dari model Anda.

Yang perlu Anda lakukan hanyalah menyetel `model` dan `fields` pada `Meta` schema Anda:


```python hl_lines="2 5 6 7"
from django.contrib.auth.models import User
from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
```

### Menggunakan Semua Field Model

Untuk menggunakan semua field dari sebuah model — Anda dapat meneruskan `__all__` ke `fields`:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    Menggunakan __all__ tidak disarankan.
    <br>
    Hal ini dapat menyebabkan terexposnya data yang tidak diinginkan secara tidak sengaja (seperti password yang di-hash pada contoh di atas).
    <br>
    Rekomendasi umum - gunakan `fields` untuk mendefinisikan secara eksplisit daftar field yang ingin Anda tampilkan di API Anda.

### Mengeksclude Field Model

Untuk menggunakan semua field **kecuali** beberapa saja, Anda dapat menggunakan konfigurasi `exclude`:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'user_permissions']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     email: str
#     is_superuser: bool
#     ... and the rest

```

### Meng-override Field

Untuk mengubah anotasi default pada beberapa field, atau menambahkan field baru, cukup gunakan properti beranotasi seperti biasa.
```python hl_lines="1 2 3 4 8"
class GroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSchema(ModelSchema):
    groups: List[GroupSchema] = []

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

```


### Membuat Field Menjadi Opsional

Untuk operasi API PATCH, Anda biasanya perlu membuat semua field sebuah schema menjadi opsional. Untuk melakukannya, Anda dapat menggunakan konfigurasi fields_optional

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

Anda juga dapat mendefinisikan hanya beberapa field tertentu menjadi opsional alih-alih semuanya:
```python
     fields_optional = ['description']
```

!!! done

    Lanjutkan ke bab berikutnya! **[Menghasilkan Schema Secara Dinamis](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
